# Ergasia_1_E16028_Gkiontsari_Charilaos
## installation
Η βάση δεδομένων InfoSys περιέχει 3 collections:
* την collection Students στην οποία αντέγραψα τα στοιχεία του Students.json ακολουθώντας τις οδηγίες των διαφανειών
* την collection Users στην οποία αποθηκεύω τους χρήστες που κάνουν sign up
* την collection uuids την οποία χρησιμοποιώ για το user authentication 

### Ερώτημα 1
Με την `collection.update` και χρησιμοποιώντας την upsert προσθέτω τον καινούργιο χρήστη στην βάση δεδομένων μόνο στην περίπτωση που δεν υπάρχει άλλος χρήστης με τα ίδια στοιχεία. 
2 προβλήματα υπάρχουν με αυτό<br/>
* το πρώτο είναι το ότι δεν μπόρεσα να εμφανίσω το κατάλληλο μήνυμα 
* το δεύτερο είναι το ότι για να μπορέσει να μπει ο καινούργιος χρήστης αρκεί να έχει διαφορετικό password με αποτέλεσμα να μπορούν να μπούν 2 users με το ίδιο username (13/5 δεν έχω βρεί ακόμα τρόπο να το φτιάξω)

### Ερώτημα 2
Ψάχνω τον συνδυασμό του username και password και αφού τον βρω κάνω generate ενα uuid μέσω της create_session το αποθηκεύω στην user_uuid και αποθηκεύω στην res το username και το user_uuid, στη συνέχεια τα ίδια στοιχεία τα προσθέτω στην βάση δεδομένων uuids για να τα χρησιμοποιήσω για το user authentication αργότερα. Επιπλέον κάθε φορά που το πρόγραμμα τρέχει η βάση δεδομένων αδειάζει απο στοιχεία με την `uuids.delete_many({})`<br/>
Αν ο συνδυασμός δεν βρεθεί εμφανίζεται ανάλογο μήνυμα


### Ερώτημα 3
Έκανα μια αλλαγή στην `is_session_valid(user_uuid)` κάνοντας return το uuid που θα βρεθεί στην collection uuids το οποίο θα είναι ένα μοναδικό εφόσον η βάση δεδομένων αδειάζει κάθε φορά που τρέχει το πρόγραμμα και θα έχει στοιχεία μέσα μόνο σε περίπτωση που ο χρήστης έχει κάνει login με επιτυχία. Σε περίπτωση που ο χρήστης δεν έχει κάνει login εμφανίζεται ανάλογο μήνυμα. <br/>
Βρίσκω μέσα στην students τον φοιτητή με το email που παίρνω απο το request, τον αποθηκεύω σε μια list την οποία αποθηκεύω στη students. Ύστερα επιστρέφω τα δεδομένα του φοιτητή.

### Ερώτημα 4
Με τον ίδιο τρόπο που κάνω authenticate τον χρήστη στο 3ο ερώτημα κάνω και σε αυτό.<br/>
Βρίσκω μέσα στην students όλους τους φοιτητές με έτος γέννησης 1991, τους αποθηκεύω σε μια list την οποία αποθηκεύω στη students. Ύστερα επιστρέφω τα δεδομένα των φοιτητών.

### Ερώτημα 5
Έκανα το ίδιο με το τέταρτο ερώτημα αλλάζοντας το query

### Ερώτημα 6
Με τον ίδιο τρόπο που κάνω authenticate τον χρήστη στο 3ο ερώτημα κάνω και σε αυτό.<br/>
Κάνω αναζήτηση στην students το email του φοιτητή και το αν ο φοιτητής με το email αντιστοιχεί σε χρήστη που έχει κάποια διεύθυνσή χρησιμοποιώντας την `$exists`. Υστερα επιστρέφει στο response τα στοιχεία email, name ,address.street και address.postcode.

### Ερώτημα 7 
Με τον ίδιο τρόπο που κάνω authenticate τον χρήστη στο 3ο ερώτημα κάνω και σε αυτό.<br/>
Κάνω αναζήτηση στην students για να βρω το email με την `collection.find_one` ύστερα με την `delete_one` διαγράφω τον φοιτητή απο τη βάση δεδομένων. Τέλος επιστρέφω το ανάλογο μήνυμα.

### Ερώτημα 8
Με τον ίδιο τρόπο που κάνω authenticate τον χρήστη στο 3ο ερώτημα κάνω και σε αυτό.<br/>
Αρχικά φτιάχνω ενα dictionary courses στο οποίο αποθηκευώ τα δεδομένα απο το request, ύστερα ψάχνω τον φοιτητή με το email απο το request. Εφόσον βρεθεί τα courses προστίθενται σε αυτόν

### Ερώτημα 9
Με τον ίδιο τρόπο που κάνω authenticate τον χρήστη στο 3ο ερώτημα κάνω και σε αυτό.<br/>
Αρχικά ψάχνω αν υπάρχει φοιτητής με το email στο request και με την `#Exists` ελέγχω αν υπάρχουν courses. Εφόσον υπάρχει παίρνω τα στοιχεία email, name και courses και τα επιστρέφω.
<br/>
Δεν ήξερα πως να επιστρέψω μόνο τα περασμένα courses(θεώρησα ότι είναι αυτά με βαθμό 5+) -Στις 13/5 δεν έχω βρει ακόμα λύση



