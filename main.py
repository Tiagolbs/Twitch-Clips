from twitchUtils import clips_request

def menu():
    print("NOME EXAMPLE\n")
    gameName = input("Game name: ")
    clipsLimit = input("How many clips to download? (max 100): ")
    clipsPeriod = input("Clips Period (day, week, month, all): ")

    clips_request(gameName, clipsLimit, clipsPeriod)

if __name__ == '__main__':
    menu()