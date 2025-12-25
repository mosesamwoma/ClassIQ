# Flask Task Manager 📝

> **Status:** 🚧 Work in Progress

A simple yet functional task management web application built with Flask, HTML, and CSS. This project demonstrates fundamental CRUD operations with a clean and intuitive user interface.

## 🌟 Features

- ✅ Create new tasks with descriptions
- 📋 View all tasks in an organized list
- ✏️ Update/Edit existing tasks
- ✔️ Mark tasks as complete or incomplete
- 🗑️ Delete tasks
- 💾 Persistent storage using SQLite database
- 🎨 Clean and responsive UI design

## 🛠️ Technologies Used

- **Backend:** Flask (Python web framework)
- **Database:** SQLite with SQLAlchemy ORM
- **Frontend:** HTML5, CSS3
- **Template Engine:** Jinja2

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/mosesamwoma/flask-todo-app.git
   cd flask-todo-app
   ```

2. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` doesn't exist, install manually:
   ```bash
   pip install Flask
   pip install Flask-SQLAlchemy
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## 🎯 Usage

### Adding a Task
1. Enter your task description in the input field
2. Click the "Add Task" button
3. The task will appear in your task list

### Updating a Task
1. Click the "Update" button next to the task
2. Modify the task description
3. Save the changes

### Completing a Task
1. Click the checkbox or "Complete" button
2. The task status will update

### Deleting a Task
1. Click the "Delete" button next to the task
2. The task will be removed from the list

## 🗄️ Database Schema

The application uses a simple SQLite database with the following schema:

**Todo Table:**
- `id` (Integer, Primary Key)
- `title` (String, max 200 characters)
- `complete` (Boolean, default: False)
- `date_created` (DateTime, auto-generated)

## 🎨 Styling

The application features custom CSS styling for:
- Responsive layout
- Clean typography
- Interactive buttons and forms
- Task list organization
- Visual feedback for completed tasks

## 🔜 Roadmap (Future Enhancements)

- [ ] User authentication and authorization
- [ ] Task categories/tags
- [ ] Due dates and reminders
- [ ] Priority levels
- [ ] Search and filter functionality
- [ ] Dark mode toggle
- [ ] Export tasks to CSV/PDF
- [ ] REST API endpoints
- [ ] Mobile app version

## 🤝 Contributing

Contributions are welcome! This project is still under development. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Moses Amwoma**
- GitHub: [@mosesamwoma](https://github.com/mosesamwoma)

## 🙏 Acknowledgments

- Flask documentation and community
- SQLAlchemy documentation
- All contributors and testers

---

**Note:** This project is currently under active development. Features and documentation may change as the project evolves.

## 📧 Contact

For questions or feedback, please open an issue on the GitHub repository.

**Happy Task Managing! 🎉**
