# WebGIS US Population Dashboard

## Abstract (چکیده)
این پروژه یک سامانه اطلاعات مکانی تحت وب (WebGIS) است که با هدف نمایش و تحلیل داده‌های جمعیتی ایالات متحده آمریکا توسعه یافته است. معماری سیستم بر پایه **Flask Microframework** در Backend و کتابخانه **Leaflet.js** در Frontend استوار است. تمرکز اصلی این پروژه بر حل چالش‌های ارتباطی با سرویس‌های نقشه خارجی (WMS)، مدیریت احراز هویت کاربران و ارائه رابط کاربری مدرن مبتنی بر **Glassmorphism** می‌باشد.

---

## Technical Architecture (معماری فنی)

### 1. Backend: Flask & Proxy Implementation
هسته اصلی سیستم با زبان **Python** و فریم‌ورک **Flask** پیاده‌سازی شده است. یکی از چالش‌های اصلی در توسعه WebGIS، محدودیت‌های امنیتی مرورگر (CORS Policy) و محدودیت‌های شبکه در دسترسی به سرویس‌های OGC استاندارد خارجی است.
برای رفع خطای `500 Internal Server Error` و `ERR_CONNECTION_RESET` در زمان فراخوانی لایه‌های WMS از سرور `ahocevar.com`، یک مکانیزم **Reverse Proxy** داخلی طراحی شد.
- **مسیر `/proxy_wms`:** این End-point درخواست‌های تایل نقشه (GetMap) و اطلاعات توصیفی (GetFeatureInfo) را از کلاینت دریافت کرده، در سمت سرور با استفاده از کتابخانه `requests` به سرور اصلی ارسال می‌کند و پاسخ را (بدون تغییر هدرهای امنیتی مزاحم) به مرورگر باز می‌گرداند.

### 2. Frontend: Leaflet & UI/UX
- **Map Rendering:** از کتابخانه **Leaflet** برای نمایش نقشه تعاملی استفاده شده است.
- **UI Design Pattern:** رابط کاربری بر اساس ترند طراحی **Glassmorphism** بازطراحی شده است که شامل المان‌های نیمه‌شفاف (Translucent)، افکت `backdrop-filter: blur` و سایه‌های نرم جهت القای عمق است.
- **Interactivity:** قابلیت کلیک روی عوارض (Feature Selection) و نمایش اطلاعات توصیفی در قالب Modal‌های پویا (Dynamic Modals) پیاده‌سازی شده است.

### 3. Database & Authentication
- مدیریت پایگاه داده با **SQLite** و از طریق **SQLAlchemy ORM** انجام می‌شود.
- مکانیزم احراز هویت (Authentication) شامل ثبت‌نام و ورود کاربران است که پسوردهای ورودی را با استفاده از الگوریتم‌های استاندارد **Hashing** (کتابخانه `werkzeug.security`) ایمن‌سازی می‌کند.

---

## Project Structure (ساختار پروژه)
```text
WebGIS-Project/
├── app.py                 # Main Application Controller & Proxy Logic
├── requirements.txt       # Project Dependencies
├── .gitignore             # Git Configuration
├── instance/
│   └── database.db        # SQLite Database (Auto-generated)
├── static/
│   ├── css/               # Custom Stylesheets
│   └── images/            # Assets (Backgrounds, Logos)
└── templates/
├── login.html         # Login Page (Glassmorphism)
├── signup.html        # Signup Page
└── map.html           # Main Dashboard (Leaflet + WMS)

---

## Key Features (قابلیت‌های کلیدی)

1.  **Secure Authentication System:** سیستم ورود و خروج با قابلیت Hashing رمز عبور و Session Management.
2.  **WMS Proxy Handler:** دور زدن محدودیت‌های CORS و فیلترینگ شبکه برای لایه‌های مکانی.
3.  **Interactive Attribute Query:** پشتیبانی از درخواست `GetFeatureInfo` برای دریافت اطلاعات توصیفی (جمعیت، مساحت، نام ایالت) با کلیک روی نقشه.
4.  **Responsive Design:** طراحی واکنش‌گرا با استفاده از **Bootstrap 5**.
5.  **UX Enhancements:** قابلیت Show/Hide Password و بازخوردهای بصری خطا (Flash Messages).

---

## Installation Guide (راهنمای نصب و اجرا)

برای اجرای لوکال پروژه، مراحل زیر را در ترمینال دنبال کنید:

### 1. Clone Repository
bash
git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME

### 2. Create Virtual Environment
پیشنهاد می‌شود یک محیط مجازی ایزوله ایجاد کنید:
bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

### 3. Install Dependencies
نصب پکیج‌های مورد نیاز شامل `Flask`, `Requests`, `SQLAlchemy`:
bash
pip install -r requirements.txt

### 4. Run Application
bash
python app.py
سپس مرورگر را باز کرده و به آدرس `http://127.0.0.1:5000` مراجعه کنید.

---

## Deployment (استقرار)

این پروژه برای اجرا روی پلتفرم‌های ابری مانند **PythonAnywhere** بهینه‌سازی شده است.
- **WSGI Configuration:** فایل پیکربندی WSGI باید به مسیر پروژه و `app.py` اشاره کند.
- **Static Files:** مسیر فایل‌های استاتیک باید در پنل هاستینگ به درستی نگاشت (Map) شود.
- **Database:** فایل `database.db` باید در پوشه‌ای با دسترسی Write قرار داشته باشد.

---

## Troubleshooting (رفع اشکال)

- **خطای `ERR_CONNECTION_REFUSED`:** مطمئن شوید سرور Flask در حال اجراست (`python app.py`).
- **عدم نمایش نقشه:** اتصال اینترنت و وضعیت سرور `ahocevar.com` را بررسی کنید. در صورت استفاده در ایران، فعال بودن VPN سیستم جهت عملکرد صحیح Proxy سرور الزامی است.
- **مشکل در Login:** دیتابیس `instance/database.db` را حذف کرده و مجدداً برنامه را اجرا کنید تا دیتابیس بازسازی شود.

---

## License
This project is open-source and available under the MIT License.
