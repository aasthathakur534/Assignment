
import requests
import matplotlib.pyplot as plt

API_URL = "https://jsonplaceholder.typicode.com/users"


def fetch_student_scores():
    """Fetch sample users and assign demonstration scores."""
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()

    users = response.json()

    # Assumption: This API contains users, not actual student scores.
    # These scores are synthetic demonstration data.
    scores = [72, 85, 68, 90, 78, 95, 81, 74, 88, 79]

    students = []

    for user, score in zip(users, scores):
        students.append({
            "name": user["name"],
            "score": score
        })

    return students


def calculate_average(students):
    """Calculate the mean of the student scores."""
    if not students:
        raise ValueError("No student scores are available.")

    total = sum(student["score"] for student in students)
    return total / len(students)


def create_bar_chart(students, average):
    """Plot scores and save the chart."""
    names = [student["name"] for student in students]
    scores = [student["score"] for student in students]

    plt.figure(figsize=(12, 6))
    plt.bar(names, scores, label="Student score")
    plt.axhline(
        average,
        linestyle="--",
        label=f"Average: {average:.2f}"
    )

    plt.xlabel("Student")
    plt.ylabel("Test score")
    plt.title("Student Test Scores")
    plt.ylim(0, 100)
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    plt.savefig("student_scores.png")
    plt.show()


def main():
    try:
        students = fetch_student_scores()
        average = calculate_average(students)

        print("Student scores:")
        for student in students:
            print(f"{student['name']}: {student['score']}")

        print(f"\nAverage score: {average:.2f}")

        create_bar_chart(students, average)
        print("Chart saved as student_scores.png")

    except requests.RequestException as error:
        print(f"API request failed: {error}")

    except (ValueError, KeyError, TypeError) as error:
        print(f"Data processing error: {error}")


if __name__ == "__main__":
    main()