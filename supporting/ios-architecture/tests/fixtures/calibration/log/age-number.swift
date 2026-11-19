import os
let logger = Logger(subsystem: "com.example.app", category: "Health")
func didLoad(_ patient: Patient) {
    logger.info("Loaded record, patient age \(patient.age), heart rate \(patient.heartRate)")
}
