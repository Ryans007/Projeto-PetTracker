# **PetTracker**

A remote animal location tracking system that allows visualization and receiving alerts from monitored animals.

&nbsp;&nbsp;&nbsp;&nbsp;

## **Project Structure**

### **General Solution Description**

**PetTracker** is a remote animal location tracking system designed to assist in monitoring and efficiently managing territories and animal populations. The solution allows users, whether supervisors or administrators, to access a centralized platform to view animal positions in real time and consult historical records of these locations.

Through a flexible and adaptable system, **PetTracker** enables the identification of animal movement patterns, assisting in strategic decision-making, such as resource reallocation, pasture area adjustments, and detection of potential risk situations. Additionally, it features an alert mechanism that notifies responsible parties if an animal exceeds the defined territorial boundaries.

To ensure broad applicability, the system can be integrated with different tracking technologies, such as centralized antennas using communication protocols like LoRa or ZigBee, or individual SIM cards with mobile network communication. The best approach can vary depending on the application scenario, making **PetTracker** a versatile solution for various sectors, such as agriculture, zoos, and natural reserves.

### **1. `main.py` File**
This is the project's main file, responsible for starting the system and managing the user interface.

#### **User Classes**
- **UserRole**: Abstract class defining user roles.
- **RegularUser**: Class for common users who can view territories.
- **AdminUser**: Class for administrators with full system access.

#### **Login Function**
- `login_screen(facade)`: Manages the login screen and user authentication.

### **2. Supporting Classes**
#### **`Tracker` Class (`_class/tracker.py`)**
- Responsible for generating and saving animal locations.
- Uses **threads** to continuously generate locations and periodically save them in the database.

#### **`Animal` Class (`_class/animal.py`)**
- Represents an animal in the system.
- Each animal has a tracker (`Tracker`) that generates its positions.

#### **`Territory` Class (`_class/territory.py`)**
- Represents a territory in the system.
- Each territory can have multiple associated animals.

### **3. Design Patterns Used**
#### **Facade Pattern**
- **SystemFacade**: Centralizes and simplifies system interaction, providing a unified interface for various operations.

#### **Proxy Pattern**
- **UserProxy, AdminProxy, TerritoryProxy**: Used to cache frequently accessed objects, reducing the need for repeated database queries.

#### **Builder Pattern**
- **TerritoryBuilder**: Facilitates the creation of complex `Territory` objects, allowing step-by-step configuration of their properties.

#### **Adapter Pattern**
- **CoordinateAdapter**: Converts geographic coordinates into Cartesian components (x, y) for system use.

#### **Singleton Pattern**
- **Database**: Ensures only one instance of the database class is created, providing a global access point to this instance.

#### **Strategy Pattern**
- **UserRole**: Defines a common interface for different user roles (RegularUser and AdminUser), allowing each to have its own menu behavior.

#### **Template Method Pattern**
- **PersonTemplate**: Defines the skeleton of an algorithm in the superclass, allowing specific subclasses to implement details of the algorithm.

### **4. Database**
#### **`Database` Class (`database/database.py`)**
- Manages the SQLite database connection and operations.
- Creates and maintains necessary tables:
  - `admins`
  - `users`
  - `territories`
  - `animals`
  - `location`
  - `tracker`

&nbsp;&nbsp;&nbsp;&nbsp;

## **System Features**

### **1. Regular Users**
- Can view territories.
- Start a **thread** to simulate real-time territory visualization.

### **2. Administrators**
- Have full system access.
- Can manage **territories, users, and animals**.
- Can view territories in real-time and access historical animal location records.

&nbsp;&nbsp;&nbsp;&nbsp;

## **Rules and Limitations**

### **Login and Authentication**
- Users and administrators are authenticated using **bcrypt** for password verification.

### **Territory Management**
- Administrators can **create, view, and delete** territories.

### **User Management**
- Administrators can **create, list, and delete** users.

### **Animal Management**
- Administrators can **add, list, and delete** animals.

&nbsp;&nbsp;&nbsp;&nbsp;

## **Interactions Between Patterns**

### **Facade and Entity Classes**
- **SystemFacade** interacts with **Tracker, Animal, and Territory** to perform complex operations in a simplified manner.

### **Proxy for Caching**
- **UserProxy, AdminProxy, TerritoryProxy** cache frequently accessed objects, improving system efficiency.

### **Builder for Object Creation**
- **TerritoryBuilder** facilitates the creation of complex `Territory` objects, allowing step-by-step configuration of their properties.

### **Adapter for Coordinate Conversion**
- **CoordinateAdapter** converts geographic coordinates into Cartesian components (x, y) for system use.

### **Singleton for Database Management**
- **Database**: Uses the Singleton pattern to ensure that only one instance of the database class is created. This is done through the `__new__` method, which checks if an instance already exists before creating a new one. This pattern is useful for managing database connections centrally and efficiently.

### **Strategy for User Menu Management**
- **UserRole**: Defines a common interface for different user roles (RegularUser and AdminUser). Each concrete class implements the `show_menu` method differently, allowing each user type to have its own menu behavior. This facilitates the addition of new user types in the future without modifying existing code.

### **Template Method for Algorithm Definition**
- **PersonTemplate**: Defines the skeleton of an algorithm in the superclass, allowing specific subclasses (User and Admin) to implement details of the algorithm. Abstract methods like `save` and `delete` are defined in the superclass and implemented in the subclasses, ensuring the algorithm structure is followed while allowing variations in details.

&nbsp;&nbsp;&nbsp;&nbsp;

## **Installation and Usage**

### **Installation**
1. Clone this repository:
   ```bash
   git clone git@github.com:Ryans007/Projeto-PetTracker.git
   cd pettracker
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the main script:
   ```bash
   python main.py
   ```
### **Login Padrão**
O sistema inicia com um login padrão já configurado. Utilize as seguintes credenciais para acessar:
- **Email:** admin@admin.com
- **Senha:** admin

&nbsp;&nbsp;&nbsp;&nbsp;

## **Conclusion**
The **"PetTracker"** project is a robust animal tracking system utilizing **design patterns** to keep the code organized and efficient. It provides essential features for **territory and animal management**, with an intuitive interface for different user types.

