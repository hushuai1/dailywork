import os
import shutil
import cv2

def preprocessVideo(video_path):
    if not os.path.exists(video_frame_save_path):
        os.mkdir(video_frame_save_path)

    vidcap = cv2.VideoCapture(video_path)
    (cap, frame) = vidcap.read()

    height = frame.shape[0]
    width = frame.shape[1]

    cnt_frame = 0

    while (cap):
        cv2.imwrite(
            os.path.join(video_frame_save_path, "frame_%d.jpg" % (cnt_frame)),
            frame)
        cnt_frame += 1
        (cap, frame) = vidcap.read()
    vidcap.release()
    return width, height


def postprocess(video_frame_save_path):
    if os.path.exists(video_frame_save_path):
        shutil.rmtree(video_frame_save_path)


def extractVideoImgs(frame, video_frame_save_path, coords):
    x1, y1, x2, y2 = coords
    # get image from save path
    img = cv2.imread(
        os.path.join(video_frame_save_path, "frame_%d.jpg" % (frame)))
    # crop
    save_img = img[y1:y2, x1:x2]
    return save_img


if __name__ == "__main__":
    #for num in range(1, 34):
        num=1
        txt_path = r"GH010765[1]_Trim_gt.txt"
        video_path = r"GH010765[1]_Trim.mp4"
        reid_dst_path = r"reid"
        # if not os.path.exists(txt_path):
        #     continue

        video_name = os.path.basename(video_path).split('.')[0]
        video_frame_save_path = os.path.join(os.path.dirname(video_path),
                                             video_name)

        f_txt = open(txt_path, "r")

        width, height = preprocessVideo(video_path)

        for line in f_txt.readlines():
            bboxes = line.split(',')
            # print(len(bboxes))
            ids = []
            frame_id = int(bboxes[0])
            num_object = int(bboxes[1])
            for num_obj in range(num_object):
                # obj = 0, 1, 2
                obj_id = bboxes[1 + (num_obj) * 6 + 1]
                obj_x1 = int(bboxes[1 + (num_obj) * 6 + 2])
                obj_y1 = int(bboxes[1 + (num_obj) * 6 + 3])
                obj_x2 = int(bboxes[1 + (num_obj) * 6 + 4])
                obj_y2 = int(bboxes[1 + (num_obj) * 6 + 5])
                # process coord
                obj_x1 = max(1, obj_x1)
                obj_y1 = max(1, obj_y1)
                obj_x2 = min(width - 1, obj_x2)
                obj_y2 = min(width - 1, obj_y2)

                print("%s:%d-%d-%d-%d" %
                      (obj_id, obj_x1, obj_y1, obj_x2, obj_y2))

                # mkdir for reid dataset
                id_dir = os.path.join(reid_dst_path,
                                      video_name + "_id_" + obj_id)
                if not os.path.exists(id_dir):
                    os.mkdir(id_dir)

                # save pic
                img = extractVideoImgs(frame_id, video_frame_save_path,
                                       (obj_x1, obj_y1, obj_x2, obj_y2))
                cv2.imwrite(
                    os.path.join(id_dir, "filename_%s_frame_%d.jpg") %
                    (video_name, frame_id), img)

        f_txt.close()
        postprocess(video_frame_save_path)
