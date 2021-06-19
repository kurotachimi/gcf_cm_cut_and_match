pwd
/Users/XXX/myproject/cm_on_gcp/upload_trigger_cut_sound
@upload_trigger_cut_sound

bucket cm_sound_data

gcloud functions deploy cut_cms \
--runtime python37 \
--entry-point first_func \
--trigger-resource cm_sound_data \
--trigger-event google.storage.object.finalize

gcloud functions deploy cut_cms

gsutil cp ../test_data/tmp.mp3 gs://cm_sound_data/original_data/tbs

gsutil ls gs://cm_sound_data/
gsutil rm gs://cm_sound_data/

gcloud functions logs read cut_cms

gsutil cp ../test_data/tbs_2021_05_25_23_54.mp3 gs://cm_sound_data/
gsutil rm gs://cm_sound_data/tbs_2021_05_25_23_54.mp3

gcloud functions logs read cut_cms
