import pyzed.sl as sl
import numpy as np
import json
import cv2

class DataExtractionWrapper():

    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD1080  # Use HD1080 video mode
    init_params.coordinate_units = sl.UNIT.METER          # Set coordinate units
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP

    positional_tracking_parameters = sl.PositionalTrackingParameters()

    obj_param = sl.ObjectDetectionParameters()
    obj_param.enable_body_fitting = True            # Smooth skeleton move
    # Track people across images flow
    obj_param.enable_tracking = True
    obj_param.detection_model = sl.DETECTION_MODEL.HUMAN_BODY_FAST
    # Choose the BODY_FORMAT you wish to use
    obj_param.body_format = sl.BODY_FORMAT.POSE_18

    obj_runtime_param = sl.ObjectDetectionRuntimeParameters()
    obj_runtime_param.detection_confidence_threshold = 40

    bodies = sl.Objects()
    image = sl.Mat()
    black = np.zeros((1080,1920,4), np.uint8)
    white = np.zeros((1080,1920,4), np.uint8)


    # Enable Object Detection module

    def __init__(self) -> None:
        err = self.zed.open(self.init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            print("Camera not Found")
            exit(1)
        self.zed.enable_positional_tracking(self.positional_tracking_parameters)
        self.zed.enable_object_detection(self.obj_param)
        self.camera_info = self.zed.get_camera_information()
        self.display_resolution = sl.Resolution(min(self.camera_info.camera_resolution.width, 1920), min(
            self.camera_info.camera_resolution.height, 1080))
        self.image_scale = [self.display_resolution.width / self.camera_info.camera_resolution.width,
                            self.display_resolution.height / self.camera_info.camera_resolution.height]
        print("Camera Found!")

    def GetImage(self):
        self.zed.retrieve_image(self.image, sl.VIEW.LEFT, sl.MEM.CPU, self.display_resolution)
        image_left_ocv = self.image.get_data()
        return image_left_ocv

    def ShowImage(self):
        self.zed.retrieve_image(self.image, sl.VIEW.LEFT, sl.MEM.CPU, self.display_resolution)
        image_left_ocv = self.image.get_data()
        #mask = self.mask.get_data()
        #image_left_ocv = cv2.bitwise_and(image_left_ocv,image_left_ocv,mask = mask)
        #cv_viewer.render_2D(image_left_ocv,self.image_scale,self.bodies.object_list, self.obj_param.enable_tracking, self.obj_param.body_format)
        cv2.imshow("ZED | 2D View", image_left_ocv)

    def GetBodies(self):
         if self.zed.grab() == sl.ERROR_CODE.SUCCESS:
            # Retrieve objects
            self.zed.retrieve_objects(self.bodies, self.obj_runtime_param)

    def GetDataAsJSONString(self):
        obj_list = []
        for body in self.bodies.object_list:
            obj = {
                "ID": body.id,
                "Label": body.label.name,
                "Tracking_state": body.tracking_state.name,
                "Action_state": body.action_state.name,
                "Position": body.position.tolist(),
                "Velocity": body.velocity.tolist(),
                "Dimensions": body.dimensions.tolist(),
                "Detection_confidence": body.confidence,
                "bounding_box_2d": body.bounding_box_2d.tolist(),
                "bounding_box_3d": body.bounding_box.tolist(),
                "Head_position": body.head_position.tolist(),
                "Head_bounding_box_2d": body.head_bounding_box_2d.tolist(),
                #"Mask" : body.mask.tolist()
            }
            obj_list.append(obj)
        return json.dumps(obj_list)
    
    def LoadDataFromZed(self):
        if self.zed.grab() == sl.ERROR_CODE.SUCCESS:
            self.zed.retrieve_objects(self.bodies, self.obj_runtime_param)
            self.zed.retrieve_image(self.image, sl.VIEW.LEFT, sl.MEM.CPU, self.display_resolution)

    def ApplyBodyMasksToFrame(self):
        #self.white.fill(255)
        self.black.fill(0)
        #self.black = np.zeros((720,1280,4), np.uint8)
        image = self.image.get_data()
        for body in self.bodies.object_list:
            if body.mask.is_init():
                mask_data = body.mask.get_data()
                mask_data = cv2.merge((mask_data,mask_data,mask_data,mask_data))
                bb2d = body.bounding_box_2d
                bb2d = bb2d.astype('int16')
                x1 = bb2d[0,0]
                y1 = bb2d[0,1]
                x2 = bb2d[2,0]
                y2 = bb2d[2,1]
                #x1,y1,x2,y2 = bb2
                cropped_image = image[y1:y2, x1:x2]
                masked_bbox_image = cv2.bitwise_and(cropped_image, mask_data)
                self.black[y1:y2, x1:x2] = masked_bbox_image
        return self.black 
        #return self.white
    
    def Close(self):
        self.zed.disable_object_detection()
        self.zed.disable_positional_tracking()
        self.zed.close()