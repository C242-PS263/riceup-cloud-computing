deploy:
	gcloud functions deploy pubsub-backend-functions \
	--gen2 \
	--runtime=python311 \
	--region=us-central1 \
	--source=. \
	--entry-point=subscribe \
	--trigger-topic=set-predict-crop-yield-advice

