import sys
import urllib.request
from twitch import TwitchClient
from twitchAPI import TwitchApiConnection
from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip, concatenate_videoclips

def clips_request(gameName, clipsLimit, clipsPeriod):
    """ Faz requisição dos clips mais vistos na Twitch.tv, em determinado periodo, do jogo escolhido
        :param gameName: nome do jogo
        :param clipsLimit: numero de clips a serem baixados
        :param clipsPeriod: periodo dos clips a serem baixados  (day, week, month, all)
    """

    try:
        client = TwitchApiConnection()
    except:
        print("Erro na conexão com a Twitch")
        exit(1)

    try:
        clips = client.clips.get_top(game=str(gameName), limit=int(clipsLimit), period=str(clipsPeriod))
    except Exception as error:
        print(error)
        exit(1)

    clips_download(clips)

def clips_download(clips):
    """ Faz o download dos clips em formato .mp4, para a pasta videos
        :param clips: retorno da requisição da API da Twitch.tv
    """

    file_names = []
    file_names_clips = []

    for i in range(len(clips)):
        thumb_url = clips[i].thumbnails['medium']
        mp4_url = thumb_url.split("-preview",1)[0] + ".mp4"

        name = clips[i].broadcaster['display_name'] + "_" + clips[i].title
        file_names.append(name)
        file_names_clips.append(clips[i].broadcaster['display_name'] + " - " + clips[i].title)

        try:
            urllib.request.urlretrieve(mp4_url, "videos/" + name + ".mp4", reporthook=dl_progress)
        except:
            print("Erro ao baixar o clip: ", name)
            exit(1)

    concatenate_clips(file_names, file_names_clips)

def concatenate_clips(file_names, file_names_clips):
    """ Adiciona um texto em cada clip, com o nome do autor e o título do clip, então compila todos os clips em um único video
        :param file_names: nome dos arquivos dos clips baixados
        :param file_names_clips: texto para escrever nos clips
    """

    clips_text = []

    for i in range(len(file_names)):
        clip = VideoFileClip("videos/" + file_names[i] + ".mp4")
        clip = clip.subclip().resize( (1920,1080) )

        txt_clip = TextClip(txt = file_names_clips[i], fontsize = 109, font = "Tahoma-Bold", color = 'white').resize(0.33).set_position('bottom').set_duration(5)  

        try:
            video = CompositeVideoClip([clip, txt_clip])
        except:
            print("Erro ao adicionar descricao ao clip", file_names[i])
            aux = input("Deseja continuar? (y/n): ")
            if aux == "y":
                video = clip
            else:
                exit(1)

        clips_text.append(video)
    
    final = concatenate_videoclips(clips_text) 
    
    try:
        final.write_videofile("videos/final.mp4")
    except:
        print("Erro ao salvar arquivo")
        exit(1)

def dl_progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%" % percent)
    sys.stdout.flush()