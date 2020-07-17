def josephus_procedural(number_of_people: int, kill_at: int, start_at: int):
    people = []
    position = start_at % number_of_people

    for i in range(number_of_people):
        people.append(i+1)
    
    counter = 1

    while len(people) > 1:
        if position >= len(people):
            position = 0
        
        if counter % kill_at == 0:
            people.pop(position)
            counter = 1
        else:
            position += 1
            counter += 1
    
    if len(people) == 1:
        print("Last man standing: " + str(people[0]))
        return

def josephus_recursive(number_of_people: int, kill_at: int):

    if number_of_people == 1:
        return 1
    else:
        return (josephus_recursive(number_of_people - 1, kill_at) + kill_at - 1) % number_of_people + 1