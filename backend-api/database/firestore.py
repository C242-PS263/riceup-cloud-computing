from google.cloud import firestore

firestore_db = firestore.Client()
diseases_ref = firestore_db.collection(u'diseases')
