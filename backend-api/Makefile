deploy:
	gcloud builds submit --tag gcr.io/riceup-441906/riceup-backend
	gcloud run deploy riceup-backend --image gcr.io/riceup-441906/riceup-backend \
		--platform managed \
		--allow-unauthenticated \
		--region us-central1 \
		--network default \
		--subnet default \
		--add-volume name=model_mnt,type=cloud-storage,bucket=riceup-model-storage \
		--add-volume-mount volume=model_mnt,mount-path=/workspace/storage/models