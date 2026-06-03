# Precision Beef - Animal Behaviour Classification

The data set contains sensor data for three cattle behaviours, (`Eating`, `Rumination` and `Other`). In particular, it contains 18 animals over three farm trials in the Easter Howgate Farm, Edinburgh, UK.


Each animal is assigned a unique identifier `XX` in the range `01`-`18` and is equipped with 2 devices:

* Afimilk Silent Herdsman Collar
* Rumiwatch Halter


## Afimilk Silent Herdsman Collar

The collar provides the raw acceleration traces from a 3-axis MEMs accelerometer at frequency of 10 Hz. The data for the collar are recorded in `CSV` format in the corresponding files `accel-XX.csv` where `XX` represents the animal identifier. Each file contains 4 columns as follows:


| Column Name | Description |
|:-----------:|-------------|
| timestamp   | The date and time the data were recorded. The timestamp is provided in ISO 8601 with no T i.e. YYYY-MM-DD HH:mm:ss.SSS |
| x           | Acceleration in the x-direction in mg |
| y           | Acceleration in the y-direction in mg |
| z           | Acceleration in the z-direction in mg |

The device is oriented in the following manner. The x-axis is oriented parallel to the animal body (parallel to the ground). The y-axis is oriented vertical to the animal body (perpendicular to the ground). The z-axis is oriented perpendicular to the animal body (parallel to the ground).

## Rumiwatch Halter

The halter measures the pressure created by the jaw movements and provides classifications at frequency of 10 Hz. The data for the halter are recorded in `CSV` format in the corresponding files `halter-XX.csv` where `XX` represents the animal identifier. Each file contains 2 columns as follows:

| Column Name    | Description |
|:--------------:|-------------|
| timestamp      | The date and time the data were recorded. The timestamp is provided in ISO 8601 with no T i.e. YYYY-MM-DD HH:mm:ss.SSS |
| classification | Behaviour classification as predicted by the Rumiwatch Halter. Note that device predicts Eating and Drinking separately but for the purposes of this study drinking events have been replaced with Eating. |

After pre-processing the halter provides 3 classifications with the following label mapping:

| Classification Label | Description          |
|:--------------------:|----------------------|
| 0                    | Other behaviour      |
| 1                    | Ruminating           |
| 2                    | Eating (or Drinking) |

Note that the number of `Drinking` samples that have been replaced with `Eating` are shown in the summary table.

## Summary Table
The table below summarize the data available for each animal and wether or not the animal was in the test set. For the halter the number of `Drinking` samples that have been replaced with `Eating` are shown in the last column.


| Animal ID |  Farm Trial ID | Test  | Collar Filename     | Collar Start Timestamp            | Collar End Timestamp              | Halter Filename    | Halter Start Timestamp          | Halter End Timestamp            |   # of Drinking Samples Replaced (Halter) |
|---:|-------------:|:-------------|:-------------|:---------------------------|:---------------------------|:--------------|:---------------------------|:---------------------------|------------------------:|
|  1 |            1 | No           | accel-01.csv | 2015-06-12 13:30:00 | 2015-06-29 08:29:59 | halter-01.csv | 2015-06-12 13:30:00 | 2015-06-29 08:29:59 |                   35500 |
|  2 |            1 | No           | accel-02.csv | 2015-06-12 13:30:00 | 2015-06-17 21:29:59 | halter-02.csv | 2015-06-12 13:30:00 | 2015-06-17 21:29:59 |                   41300 |
|  3 |            1 | No           | accel-03.csv | 2015-06-12 15:00:00 | 2015-06-25 16:29:59 | halter-03.csv | 2015-06-12 15:00:00 | 2015-06-25 16:29:59 |                   39200 |
|  4 |            1 | Yes          | accel-04.csv | 2015-06-12 14:30:00 | 2015-06-18 12:59:59 | halter-04.csv | 2015-06-12 14:30:00 | 2015-06-18 12:59:59 |                   11300 |
|  5 |            1 | No           | accel-05.csv | 2015-06-12 14:30:00 | 2015-06-17 21:59:59 | halter-05.csv | 2015-06-12 14:30:00 | 2015-06-17 21:59:59 |                   22700 |
|  6 |            1 | No           | accel-06.csv | 2015-06-12 14:30:00 | 2015-06-29 08:29:59 | halter-06.csv | 2015-06-12 14:30:00 | 2015-06-29 08:29:59 |                   64800 |
|  7 |            2 | No           | accel-07.csv | 2015-09-14 09:00:00 | 2015-09-21 07:29:59 | halter-07.csv | 2015-09-14 09:00:00 | 2015-09-21 07:29:59 |                   29300 |
|  8 |            2 | No           | accel-08.csv | 2015-09-14 09:00:00 | 2015-09-21 07:59:59 | halter-08.csv | 2015-09-14 09:00:00 | 2015-09-21 07:59:59 |                   24700 |
|  9 |            2 | No           | accel-09.csv | 2015-09-14 10:00:00 | 2015-09-21 07:59:59 | halter-09.csv | 2015-09-14 10:00:00 | 2015-09-21 07:59:59 |                   42800 |
| 10 |            2 | Yes          | accel-10.csv | 2015-09-14 10:00:00 | 2015-09-21 07:59:59 | halter-10.csv | 2015-09-14 10:00:00 | 2015-09-21 07:59:59 |                   28300 |
| 11 |            3 | Yes          | accel-11.csv | 2016-09-19 12:34:10 | 2016-09-26 09:00:47 | halter-11.csv | 2016-09-19 12:34:10 | 2016-09-26 09:00:47 |                   30200 |
| 12 |            3 | No           | accel-12.csv | 2016-10-03 12:01:47 | 2016-10-09 13:36:56 | halter-12.csv | 2016-10-03 12:01:47 | 2016-10-09 13:36:56 |                   15300 |
| 13 |            3 | No           | accel-13.csv | 2016-09-19 12:46:41 | 2016-09-26 09:50:17 | halter-13.csv | 2016-09-19 12:46:41 | 2016-09-26 09:50:17 |                   46400 |
| 14 |            3 | No           | accel-14.csv | 2016-09-12 10:04:23 | 2016-09-19 10:24:26 | halter-14.csv | 2016-09-12 10:04:23 | 2016-09-19 10:24:26 |                   60500 |
| 15 |            3 | No           | accel-15.csv | 2016-08-29 10:18:24 | 2016-09-05 09:51:43 | halter-15.csv | 2016-08-29 10:18:24 | 2016-09-05 09:51:43 |                   40200 |
| 16 |            3 | No           | accel-16.csv | 2016-09-13 10:30:38 | 2016-09-19 04:55:12 | halter-16.csv | 2016-09-13 10:30:38 | 2016-09-19 04:55:12 |                   15500 |
| 17 |            3 | No           | accel-17.csv | 2016-08-29 09:37:37 | 2016-09-05 08:44:42 | halter-17.csv | 2016-08-29 09:37:37 | 2016-09-05 08:44:42 |                   45700 |
| 18 |            3 | No           | accel-18.csv | 2016-09-05 14:14:43        | 2016-09-12 08:57:23        | halter-18.csv | 2016-09-05 14:14:43        | 2016-09-12 08:57:23        |                   26800 |
