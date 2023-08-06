#!/usr/bin/env python
"""
usage: subaligner_2pass [-h] -v VIDEO_PATH -s SUBTITLE_PATH [-l MAX_LOGLOSS] [-so] [-fos] [-tod TRAINING_OUTPUT_DIRECTORY] [-o OUTPUT] [-d] [-q]

Run two-stage alignment

optional arguments:
  -h, --help            Show this help message and exit
  -l MAX_LOGLOSS, --max_logloss MAX_LOGLOSS
                        Max global log loss for alignment
  -so, --stretch_off    Switch off stretch on subtitles for non-English speech
  -fos, --exit_segfail  Exit on any segment alignment failures
  -tod TRAINING_OUTPUT_DIRECTORY, --training_output_directory TRAINING_OUTPUT_DIRECTORY
                        Path to the output directory containing training results
  -o OUTPUT, --output OUTPUT
                        Path to the output subtitle file
  -d, --debug           Print out debugging information
  -q, --quiet           Switch off logging information

required arguments:
  -v VIDEO_PATH, --video_path VIDEO_PATH
                        Path to the video file
  -s SUBTITLE_PATH, --subtitle_path SUBTITLE_PATH
                        Path to the subtitle file
"""

import argparse
import sys
import traceback
import os


def main():
    if sys.version_info.major != 3:
        print("Cannot find Python 3")
        sys.exit(20)
    try:
        import subaligner
    except ModuleNotFoundError:
        print("Subaligner is not installed")
        sys.exit(20)

    parser = argparse.ArgumentParser(description="Run two-stage alignment")
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-v",
        "--video_path",
        type=str,
        default="",
        help="Path to the video file",
        required=True,
    )
    required_args.add_argument(
        "-s",
        "--subtitle_path",
        type=str,
        default="",
        help="Path to the subtitle file",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--max_logloss",
        type=float,
        default=float("inf"),
        help="Max global log loss for alignment",
    )
    parser.add_argument(
        "-so",
        "--stretch_off",
        action="store_true",
        help="Switch off stretch on subtitles for non-English speech",
    )
    parser.add_argument(
        "-fos",
        "--exit_segfail",
        action="store_true",
        help="Exit on any segment alignment failures",
    )
    parser.add_argument(
        "-tod",
        "--training_output_directory",
        type=str,
        default=os.path.abspath(os.path.dirname(subaligner.__file__)),
        help="Path to the output directory containing training results",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="",
        help="Path to the output subtitle file",
    )
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Print out debugging information")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Switch off logging information")
    FLAGS, unparsed = parser.parse_known_args()

    if FLAGS.video_path == "":
        print("--video_path was not passed in")
        sys.exit(21)
    if FLAGS.subtitle_path == "":
        print("--subtitle_path was not passed in")
        sys.exit(21)

    exit_segfail = FLAGS.exit_segfail
    stretch = not FLAGS.stretch_off

    from subaligner.logger import Logger
    Logger.VERBOSE = FLAGS.debug
    Logger.QUIET = FLAGS.quiet
    from subaligner.predictor import Predictor
    from subaligner.subtitle import Subtitle
    from subaligner.exception import UnsupportedFormatException
    from subaligner.exception import TerminalException

    try:
        predictor = Predictor()
        subs_list, subs, voice_probabilities, frame_rate = predictor.predict_dual_pass(
            video_file_path=FLAGS.video_path,
            subtitle_file_path=FLAGS.subtitle_path,
            weights_dir=os.path.join(FLAGS.training_output_directory, "models/training/weights"),
            stretch=stretch,
            exit_segfail=exit_segfail,
        )

        aligned_subtitle_path = "_aligned.".join(FLAGS.subtitle_path.rsplit(".", 1)) if FLAGS.output == "" else FLAGS.output
        Subtitle.export_subtitle(FLAGS.subtitle_path, subs_list, aligned_subtitle_path, frame_rate)
        print("Aligned subtitle saved to: {}".format(aligned_subtitle_path))

        log_loss = predictor.get_log_loss(voice_probabilities, subs_list)
        if log_loss is None or log_loss > FLAGS.max_logloss:
            print(
                "Alignment failed with a too high loss value: {}".format(log_loss)
            )
            exit(22)
    except UnsupportedFormatException as e:
        print(
            "{}\n{}".format(str(e), "".join(traceback.format_stack()) if FLAGS.debug else "")
        )
        sys.exit(23)
    except TerminalException as e:
        print(
            "{}\n{}".format(str(e), "".join(traceback.format_stack()) if FLAGS.debug else "")
        )
        sys.exit(24)
    except Exception as e:
        print(
            "{}\n{}".format(str(e), "".join(traceback.format_stack()) if FLAGS.debug else "")
        )
        sys.exit(1)
    else:
        exit(0)


if __name__ == "__main__":
    main()
