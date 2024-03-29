import sys
from timeit import default_timer as timer

from bruteforce import BruteForce
from dynamicprogramming import DynamicProgramming
from genetic import Genetic
from graph import Graph
from os import system, name, listdir, path

from simulatedannealing import SimulatedAnnealing


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def print_to_continue():
    input("Aby kontynuować wciśnij dowolny klawisz")


absolute_directory = path.dirname(path.realpath(__file__))


def get_script_path():
    return path.dirname(path.realpath(sys.argv[0]))


def test(graph):

    clear()
    repeats = int(input("Liczba powtórzeń: "))

    while 1:
        clear()
        print("Możliwości do wyboru:\n")
        print("1. Brute Force")
        print("2. Programowanie dynamiczne")
        print("3. Powrót do głównego menu")
        choice = input("\nPodaj numer: ")
        if choice == '1':
            start = timer()
            for x in range(repeats):
                bf = BruteForce(graph)
                bf.start(0)

            end = timer()
            time = format((end - start) / repeats, '.8f')
            print(time)
            with open(get_script_path() + '/measurements/bf_measurement.txt', 'a+') as the_file:
                the_file.write(graph.file_name + "\n" + time + "\n")
            print_to_continue()

        if choice == '2':
            start = timer()
            for x in range(repeats):
                dp = DynamicProgramming(graph)
                dp.start(0)

            end = timer()
            time = format((end - start) / repeats, '.8f')
            print(time)
            with open(get_script_path() + '/measurements/dp_measurement.txt', 'a+') as the_file:
                the_file.write(graph.file_name + "\n" + time + "\n")
            print_to_continue()

        if choice == '3':
            return


def main():
    graph = Graph()

    while 1:
        clear()
        print("Program do wyznaczania optymalnego cyklu Hamiltiona dla problemu komiwojażera\n")

        if graph.number_of_cities != 0:
            print("Liczba wierzchołków aktualnie wczytanego grafu: " + str(graph.number_of_cities) + "\n")
        else:
            print("Aktualnie nie wczytano żadnego grafu\n")
        print("Wybierz funkcjonalność")
        print("1. Wczytaj małą macierz grafu")
        print("2. Wczytaj dużą macierz grafu")
        print("3. Wyświetl macierz kosztów")
        print("4. Brute Force")
        print("5. Programowanie dynamiczne")
        print("6. Symulowane wyżarzanie")
        print("7. Algorytm genetyczny")
        print("8. Przeprowadź testy seryjne")
        print("9. Zakończ działanie programu")
        choice = input("\nPodaj numer: ")
        if choice == '1':
            clear()
            print("Lista dostępnych plików:\n-----------")
            print(*listdir(get_script_path() + "/matrixes/small/"), sep='\n')
            print("-----------")
            file_name = input("Podaj nazwę pliku z małym grafem: ")
            graph = Graph(file_name, 0)
            print("Wczytano graf z " + str(graph.number_of_cities) + " wierzchołkami\nAby kontynuwać wciśnij dowolny "
                                                                     "klawisz")
            choice = 0
            input()

        if choice == '2':
            clear()
            print("Podaj nazwę pliku z dużym grafem")
            print(*listdir(get_script_path() + "/matrixes/large/"), sep='\n')
            file_name = input()
            graph = Graph(file_name, 1)
            print("Wczytano graf z " + str(graph.number_of_cities) + " wierzchołkami")
            print_to_continue()
            choice = 0

        if choice == '3':
            clear()
            if graph.number_of_cities != 0:
                graph.display_cost_matrix()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '4':
            if graph.file_name != "":
                bf = BruteForce(graph)
                bf.starting_vertex = 0
                bf.start(0)
                print("Najlepszy cykl ma wagę: " + str(bf.best_cycle_cost))
                print("Optymalny cykl: ")
                bf.display_optimal_route()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '5':
            if graph.file_name != "":
                dp = DynamicProgramming(graph)
                dp.start(0)
                print("Najlepszy cykl ma wagę: " + str(dp.best_cycle_cost))
                print("Optymalny cykl: ")
                dp.display_optimal_route()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '6':
            if graph.file_name != "":
                t_0 = float(input("Temperatura początkowa wyżarzania: "))
                t_min = float(input("Temperatura minimalna wyżarzania: "))
                t_coefficient = float(input("Współczynnik wyżarzania z zakresu (0,1): "))
                sa = SimulatedAnnealing(graph)
                start = timer()
                sa.start(t_0, t_min, t_coefficient)
                end = timer()
                time = format(end - start, '.8f')
                print(time)
                print("Najlepszy cykl ma wagę: " + str(sa.best_cycle_cost))
                print("Optymalny cykl: ")
                sa.display_optimal_route()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '7':
            if graph.file_name != "":
                size_of_population = int(input("Podaj początkową liczebność populacji: "))
                number_of_generations = int(input("Podaj liczbę pokoleń, która ma się urodzić: "))
                cross_probability = float(input("Podaj prawdopodobieństwo krzyżowania: "))
                mutation_probability = float(input("Podaj prawdopodobieństwo mutacji: "))
                # size_of_population = 10
                # number_of_generations = 150
                # cross_probability = 0.6
                # mutation_probability = 0.2
                gen = Genetic(graph)
                start = timer()
                gen.start(size_of_population, number_of_generations, cross_probability, mutation_probability)
                end = timer()
                time = format(end - start, '.8f')
                print(time)
                print("Najlepszy cykl ma wagę: " + str(gen.best_cycle_cost))
                print("Optymalny cykl: ")
                gen.display_optimal_route()
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '8':
            if graph.file_name != "":
                test(graph)
            else:
                print("Nie wczytano żadnego grafu")
            print_to_continue()

        if choice == '9':
            print_to_continue()
            clear()
            return


if __name__ == '__main__':
    main()
