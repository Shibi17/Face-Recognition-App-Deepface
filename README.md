# 🌟 Face Recognition App

![Face Recognition Banner](https://images.unsplash.com/photo-1593642532973-d31b6557fa68?fit=crop&w=1200&q=80)

A modern **Face Recognition Web Application** built with **Flask**, **DeepFace**, and **OpenCV**. This app allows you to **register faces**, **recognize unknown faces**, and keeps a **persistent gallery** of all registered and recognized images.  

---

## 🔹 Features

- **Register Faces**  
  Upload an image with a name, and save it persistently on the server or cloud.

- **Recognize Faces**  
  Upload an image and the app detects, matches, and displays recognized faces with **confidence scores**.

- **Cloud Support**  
  All registered images can be uploaded and recognized from the cloud.

- **Session-Persistent Gallery**  
  View all registered and recognized faces in a beautiful gallery. Previously uploaded images remain visible.

- **Audit Logging**  
  Tracks all actions (register & recognize) with details like username, filename, recognition type, and confidence.

- **Stylish UI**  
  Clean and modern interface with responsive layout and live image previews.

---

## 🏗️ Tech Stack

- **Backend:** Python, Flask  
- **Face Recognition:** DeepFace (Facenet)  
- **Image Processing:** OpenCV, NumPy  
- **Cloud Storage:** AWS S3 / Local fallback  
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)  

---
