# DCL Employee Documents Notification

Manages Employee Related Documents (e.g., passports, visas, licenses) with Expiry Notifications. This is a fully standalone custom module designed to run side-by-side with the default `oh_employee_documents_expiry` module without database or UI conflicts.

---

## 🌟 Key Features
1. **No Conflicts (Prefix `dcl_` / `dcl.`)**:
   - All models (`dcl.document.type`, `dcl.hr.employee.document`, `dcl.hr.document`), database tables, and view records are prefixed to prevent name clashes.
2. **Dedicated Security Role**:
   - Includes a user access control group: **`DCL Documents / Manager`**. Only users assigned to this group can view, create, or modify the document records and menus.
3. **HR Document Reminder Access (Settings)**:
   - Configurable list of multiple global recipients in **Settings ➔ Employees (HR)** who will receive expiry emails for all employee documents.
4. **Enhanced UI**:
   - A distinct **HR Documents** smart button with a relevant identity card icon (`fa-id-card-o`) on the employee form view.
   - Separate menu items labeled **Documents (DCL)**, **Document Types (DCL)**, and **Document Templates (DCL)** to differentiate from base modules.

---

## 🔧 Installation & Configuration
1. **Module Installation**:
   - Place this directory in your Odoo custom addons path.
   - Go to Odoo **Apps**, click **Update Apps List**, and search for `DCL Employee Documents Notification` (Technical name: `dcl_employee_documenst_notification`).
   - Click **Install**.

2. **Access Control Settings**:
   - Go to **Settings ➔ Users & Companies ➔ Users**.
   - Edit a user, and check the **DCL Documents** field: select **Manager** to give them access to manage employee documents.

3. **Global Recipients Configuration**:
   - Go to **Settings ➔ Employees**.
   - Find **HR Document Reminder Access**.
   - Select the employees who should globally receive document expiry reminder emails.

---

## ⚙️ Usage
1. **Document Types**:
   - Go to **HR ➔ Configuration ➔ Document Types (DCL)** to add custom document categories (e.g. Visa, Driving License).
2. **Document Templates**:
   - Go to **HR ➔ Document Templates (DCL)** to define document templates for automated assignments.
3. **Employee Documents**:
   - On any employee's profile, click the **HR Documents** smart button to add, track, and attach scanned copies of documents with specific expiry dates and reminder types.
