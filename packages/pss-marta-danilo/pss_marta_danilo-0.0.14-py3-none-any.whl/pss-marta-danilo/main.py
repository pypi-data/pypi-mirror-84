import matplotlib.pyplot as plt
import media
import scambia
import MySQLdb as sql
import argparse


# per far funzionare su gitlab usare questi valori
# Host: mysql
# User: runner
# Password: Databasepss20/21 #noqa
# Database: assignment1
def get_im_from_db(indice, hostname):
    db = sql.connect(host=hostname, user="runner", passwd="Databasepss20/21", db="assignment1") # nosec
    #db = sql.connect(host="127.0.0.1", user="root", passwd=MYSQL_PASS, db=MYSQL_DB) # noqa
    cursor = db.cursor()
    percorso = "SELECT percorso FROM metadata WHERE id =" + str(indice)
    cursor.execute(percorso)
    # results = cursor.fetchall()
    results = cursor.fetchone()
    image = plt.imread(str(results[0]))
    return image


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='give db hostname')
    parser.add_argument('hostname', type=str, help='the hostname')
    args = parser.parse_args

    im = get_im_from_db(2, args.hostname)

    array_medie = media.get_media(im)

    pos = array_medie.index(max(array_medie))

    new_im = scambia.scambia(im, pos)
    print("sto per stampare le immagini")
    plt.subplot(1, 2, 1)
    plt.imshow(im)
    plt.subplot(1, 2, 2)
    plt.imshow(new_im)
    plt.show()
