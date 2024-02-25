from api import worshipDB
import pprint as pp
def main():
    test = worshipDB()

    ex1 = test.get_unique_religion()

    ex2 = test.find_k_nearest(latlon=(-71.0589, 42.3601), religion='CHRISTIAN', k=10)

    ex3 = test.find_state_largest(state='MA', religion='CHRISTIAN', n=10)

    ex4 = test.plot_religion(religion='BUDDHIST')

    ex5 = test.make_map()



if __name__ == '__main__':
    main()