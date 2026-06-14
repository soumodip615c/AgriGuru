from disease_detector import predict_disease

result = predict_disease(
    r"D:\AgriGuru\input\images\test.jpg"
)

print("Disease:", result["disease"])
print("Confidence:", result["confidence"], "%")