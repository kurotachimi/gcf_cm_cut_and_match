import pandas as pd
from google.cloud import storage
from pydub import AudioSegment
from pydub.silence import split_on_silence
import datetime

import audfprint
import codecs

from google.cloud import bigquery

pklname = "fpdbase_all.pklz"


def first_func(event, context):
    file_name = event["name"]
    if file_name.endswith(".mp3"):
        print("Event ID: {}".format(context.event_id))
        print("Event type: {}".format(context.event_type))
        print("Bucket: {}".format(event["bucket"]))
        print("File: {}".format(event["name"]))
        print("Metageneration: {}".format(event["metageneration"]))
        print("Created: {}".format(event["timeCreated"]))
        print("Updated: {}".format(event["updated"]))

        timedatabase = pd.DataFrame(
            [],
            columns=[
                "path",
                "oldfilename",
                "channel",
                "date",
                "sec_type",
                "hour",
                "minutes",
                "minutes_plus",
                "newfilename",
            ],
        )
        bucket = event["bucket"]
        file_name = event["name"]
        tmp_main_file_name = "/tmp/temp.mp3"
        outputfile = "/tmp/output.txt"
        download_blob(bucket, file_name, tmp_main_file_name)
        # soundpath = tmp_main_file_name
        channel = "asahi"
        min_silence_len = 600
        thresh = -40

        print(file_name)

        # 本来ここに下のコード入れる

        ans = cm_match(tmp_main_file_name)
        print("ans; ", ans)

        with codecs.open(outputfile, "r", "utf-8", "ignore") as f:
            rows_to_insert = []
            for line in f:
                line = line.strip()
                if line.find("Matched") >= 0:
                    # print(line)
                    id_ = line.split(".mp3")[1].split("/")[-1]
                    d_split = file_name.split("_")

                    dt = datetime.datetime(
                        int(d_split[1]),
                        int(d_split[2]),
                        int(d_split[3]),
                        int(d_split[4]),
                        int(d_split[5].split(".mp3")[0]),
                    )

                    timegap_ = datetime.timedelta(
                        minutes=(
                            600
                            - float(
                                line.split("starting at ")[1]
                                .split(" s in")[0]
                                .split()[0]
                            )
                        )
                        // 60
                    )
                    actual_date = dt - timegap_

                    date = d_split[1] + "-" + d_split[2] + "-" + d_split[3]
                    time = (
                        str(actual_date.hour)
                        + ":"
                        + str(actual_date.minute)
                        + ":"
                        + "00"
                    )

                    channel = "asahi"
                    rank_ = int(line.split("rank ")[1])

                    rows_to_insert.append(
                        {
                            u"id_": id_,
                            u"date": date,
                            u"time": time,
                            u"channel": channel,
                            u"rank_": rank_,
                            u"datetime": date + " " + time,
                            u"pklz": pklname,
                        }
                    )

        # bqへStreamingInsert
        print(rows_to_insert)
        if len(rows_to_insert) > 0:
            #            print(ans, channel, origina_file_name,)

            client = bigquery.Client(project="ad-database-321502")
            table_id = "ad_database.streaming_sandbox"
            # rows_to_insert = [
            #    {u"yid": ans, u"channel": channel, u"date": origina_file_name}
            # ]

            errors = client.insert_rows_json(table_id, rows_to_insert)

            if errors == []:
                print("New rows have been added.")
            else:
                print("Encountered errors while inserting rows: {}".format(errors))

    else:
        print("Not sound data")


"""
        sound = AudioSegment.from_file(soundpath, format="mp3")
        chunks = split_on_silence(
            sound,
            min_silence_len=min_silence_len,
            silence_thresh=thresh,
            keep_silence=min_silence_len
        )
        print(len(chunks))

        total = 0
        n = 0
        sec15_list = []
        total_list = []
        for i in range(len(chunks)):  # range(1~)
            length = len(chunks[i])/1000
            total += len(chunks[i])
            minu = total // 60000
            sec = total % 60000+7000
            #       print(i,len(chunks[i])/1000,total,minu,sec ,sep = '----')

            if ((length > 14) & (length < 16.3)) | ((length > 29) & (length < 31.3)) | ((length > 59) and (length < 61.3)):
                sec15_list.append(chunks[i])
                total_list.append(minu)
            else:
                pass

        print(len(sec15_list))
        origina_file_name = file_name.split('/')[-1].split('.')[0]
        print(origina_file_name)
        # ここまで、分割後→チェックするスタイル
"""
"""#分割後秒数制限をして、テキストファイルに一括で出す試みをしたところ
        cutted_path_list = []
        for n in range(len(sec15_list)): " n=0までは成功

            test_export_path = '/tmp/temp_save_audio'+str(n)+'.mp3'
            test_sound.export(test_export_path, format="mp3", parameters=[
                            '-c:a', 'libmp3lame', '-b:a', '32k'])
            print(test_sountd)
            cutted_path_list.append(test_export_path)
        # cutted_listをテキストファイルに
        str_ = '\n'.join(cutted_path_list)
        cutted_path_list_text = '/tmp/cutted_path_list.txt'
        with open(cutted_path_list_text, 'wt') as f:
            f.write(str_)
"""


def cm_match(tmp_main_file_name):
    outputfile = "/tmp/output.txt"
    l = [
        "1",
        "match",
        "--dbase",
        pklname,
        tmp_main_file_name,
        "--find-time-range",
        "--max-matches",
        "20",
        "--search-depth",
        "100",
        "--min-count",
        "20",
        "-o",
        outputfile,
    ]

    result = audfprint.main(l)
    return "ok"


def download_blob(bucket_name, source_blob_name, destination_file_name):

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print("Blob {} downloaded to {}.".format(source_blob_name, destination_file_name))
