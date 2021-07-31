pwd
/Users/XXX/myproject/cm_on_gcp/upload_trigger_cut_sound
@upload_trigger_cut_sound

bucket ad_ntv

gcloud config set project ad-database-321502

gcloud functions deploy cut_cms_ntv \
--runtime python37 \
--entry-point first_func \
--memory 2048MB \
--region asia-northeast1 \
--trigger-resource ad_ntv \
--timeout 300s \
--trigger-event google.storage.object.finalize

gcloud functions deploy cut_cms_ntv

gcloud functions logs read cut_cms_n

gsutil cp ../test_data/tbs_2021_05_25_23_54.mp3 gs://ad_ntv/
gsutil rm gs://ad_ntv/tbs_2021_05_25_23_54.mp3

gcloud functions logs read cut_cms_ntv
