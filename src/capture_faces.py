import cv2
import os
import argparse

def capture_student_faces(student_name, student_id, capture_count=20):
    """
    Captures a set number of images for a specific student from the webcam.
    """
    # Create a clean directory name
    safe_name = f"{student_id}_{student_name.replace(' ', '_')}"
    save_dir = os.path.join("data", "known_faces", safe_name)
    
    # Create the directory if it doesn't exist
    os.makedirs(save_dir, exist_ok=True)
    
    print(f"[*] Initializing camera...")
    # Open the default webcam (index 0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("[!] Error: Could not open webcam.")
        return

    print(f"\n[*] Ready to capture {capture_count} images for: {student_name} ({student_id})")
    print("[*] Position yourself in front of the camera.")
    print("[*] Press 'C' to capture an image. Press 'Q' to quit early.\n")

    count = 0
    while count < capture_count:
        ret, frame = cap.read()
        if not ret:
            print("[!] Error: Failed to grab frame.")
            break
            
        # Display instructions on the frame
        display_frame = frame.copy()
        cv2.putText(display_frame, f"Captures: {count}/{capture_count}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(display_frame, "Press 'C' to capture | 'Q' to quit", (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Data Acquisition - Student Capture', display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('c') or key == ord('C'):
            # Save the clean frame (without text)
            file_path = os.path.join(save_dir, f"{safe_name}_{count}.jpg")
            cv2.imwrite(file_path, frame)
            count += 1
            print(f"[+] Captured {count}/{capture_count} -> {file_path}")
        elif key == ord('q') or key == ord('Q'):
            print("[-] Capture cancelled by user.")
            break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    
    if count == capture_count:
        print(f"\n[SUCCESS] Successfully captured {capture_count} images for {student_name}!")
        print(f"[*] Data saved in: {save_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Capture training images for the Attendance System")
    parser.add_argument("--name", "-n", type=str, required=True, help="Full name of the student")
    parser.add_argument("--id", "-i", type=str, required=True, help="Unique ID/Roll Number of the student")
    parser.add_argument("--count", "-c", type=int, default=20, help="Number of images to capture (default: 20)")
    
    args = parser.parse_args()
    
    capture_student_faces(args.name, args.id, args.count)
