# 👾 GitPets: Your GitHub Tamagotchi

**GitPets** is a dynamic, gamified widget designed to turn your coding consistency into a survival game! It tracks your GitHub activity over the last 7 days and reflects your productivity through a retro-style digital pet.



## 🎯 The Motivation
Coding every day can be tough. **GitPets** uses "gamification" to give you that extra push:
* **High Activity:** Your pet is glowing, happy, and full of energy! 🌟
* **Low Activity:** Your pet starts to get hungry and sad. 🦴
* **The Goal:** Don't let your pet down! Keep pushing code to keep it happy.

## 🚀 How it Works (Scoring System)
The API fetches your public events from the last **7 days** and calculates an **Activity Score**:
* **Pull Requests & Merges:** +5 points 🍕
* **Code Reviews:** +4 points
* **Issues & Comments:** +3 points
* **Commits (Push):** +2 points per commit 🍬
* **Forks & Deletions:** +1 point

## 🛠️ Built With
* **Python & Flask:** The engine that runs the API.
* **GitHub API:** To fetch real-time user activity.
* **SVG & CSS:** To render the retro console UI dynamically.
* **Pixel Art & GIFs:** Custom animations for the pet's states (Happy, OK, Sad).
* **Render:** For cloud hosting and deployment.

## choose your pet
* **molly** cat
* **spot:** beagle
* **tobby** pug

## 💻 How to add it to your Profile
To display your own GitPet on your GitHub Profile README, add the following markdown line:

```markdown
![My GitPet](https://gitpets.onrender.com/api?username=YOUR_USERNAME&petname=YOUR_CHOICE)
