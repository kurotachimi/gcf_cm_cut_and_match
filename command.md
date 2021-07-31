pwd
/Users/XXX/myproject/cm_on_gcp/upload_trigger_cut_sound
@upload_trigger_cut_sound

bucket ad_tokyo

gcloud config set project ad-database-321502

gcloud functions deploy cut_cms_tokyo \
--runtime python37 \
--entry-point first_func \
--memory 2048MB \
--region asia-northeast1 \
--trigger-resource ad_tokyo \
--timeout 300s \
--trigger-event google.storage.object.finalize

gsutil cp ../test_data/tbs_2021_05_25_23_54.mp3 gs://ad_tokyo/
gsutil rm gs://ad_tokyo/tbs_2021_05_25_23_54.mp3

gcloud functions logs read cut_cms_asahi
