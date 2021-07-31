pwd
/Users/XXX/myproject/cm_on_gcp/upload_trigger_cut_sound
@upload_trigger_cut_sound

bucket ad_fuji

gcloud config set project ad-database-321502

gcloud functions deploy cut_cms_fuji \
--runtime python37 \
--entry-point first_func \
--memory 2048MB \
--region asia-northeast1 \
--trigger-resource ad_fuji \
--timeout 300s\
--trigger-event google.storage.object.finalize

gcloud functions deploy cut_cms_fuji

gcloud functions logs read cut_cms_fuji

gsutil cp ../test_data/tbs_2021_05_25_23_54.mp3 gs://ad_fuji/
gsutil rm gs://ad_tbs/tbs_2021_05_25_23_54.mp3

gcloud functions logs read cut_cms_fuji

#f15 ver
gcloud functions deploy cut_cms_f15 \
--runtime python37 \
--entry-point first_func \
--trigger-resource cm_sound_data \
--trigger-event google.storage.object.finalize
