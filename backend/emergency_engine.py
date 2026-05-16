class EmergencyEngine:

    def __init__(self, alert_service, sensor_service):
        self.alert_service = alert_service
        self.sensor_service = sensor_service

        self.last_fall_state = False

    def update(self, camera_fall_detected):

        pir_detected = self.sensor_service.read_pir()
        loud_sound = self.sensor_service.is_loud_sound()

        # Demo logic:
        # Camera detects fall + PIR detects presence/movement
        if camera_fall_detected and pir_detected:

            if self.last_fall_state is False:
                print("EmergencyEngine: camera fall + PIR detected")
                self.alert_service.detect_possible_fall()

            self.last_fall_state = True

        # Optional: simulated sound strengthens emergency suspicion
        elif camera_fall_detected and loud_sound:

            if self.last_fall_state is False:
                print("EmergencyEngine: camera fall + simulated sound detected")
                self.alert_service.detect_possible_fall()

            self.last_fall_state = True

        else:
            self.last_fall_state = False

        self.alert_service.update()