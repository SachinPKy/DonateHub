{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Add Donation | DonateHub</title>

    <link rel="icon" href="{% static 'favicon.ico' %}">
    <link rel="icon" type="image/png" sizes="16x16" href="{% static 'images/favicon-16x16.png' %}">
    <link rel="icon" type="image/png" sizes="32x32" href="{% static 'images/favicon-32x32.png' %}">
    <link rel="apple-touch-icon" href="{% static 'images/apple-touch-icon.png' %}">
    <link rel="manifest" href="{% static 'site.webmanifest' %}">

    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
    />

    <style>
      body {
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
          url("{% static 'images/bg.png' %}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        min-height: 100vh;
        padding: 15px;
      }

      .donation-card {
        max-width: 650px;
        margin: 70px auto;
        padding: 35px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.96);
        box-shadow: 0 10px 35px rgba(0, 0, 0, 0.3);
      }

      .donation-title {
        font-weight: bold;
        color: #0d6efd;
      }

      .ai-btn {
        font-size: 0.9rem;
      }
    </style>
  </head>

  <body>
    <div class="container">
      <div class="donation-card">
        <h3 class="text-center donation-title mb-3">Add Donation</h3>

        <p class="text-center text-muted mb-4">
          Help communities by donating reusable items such as clothes, books,
          toys, and essential supplies.
        </p>

        <!-- IMPORTANT: enctype added -->
        <form method="post" enctype="multipart/form-data">
          {% csrf_token %}

          <!-- CATEGORY -->
          <div class="mb-3">
            <label class="form-label">Donation Category</label>
            <input
              type="text"
              class="form-control"
              name="category"
              id="id_category"
              required
            />
          </div>

          <!-- DESCRIPTION -->
          <div class="mb-3">
            <label class="form-label">Donation Description</label>
            <textarea
              class="form-control"
              name="description"
              id="id_description"
              rows="4"
              required
            ></textarea>

            <button
              type="button"
              class="btn btn-info btn-sm mt-2 ai-btn"
              onclick="getCategory()"
            >
              🤖 Suggest Category (AI)
            </button>

            <button
              type="button"
              class="btn btn-warning btn-sm mt-2 ai-btn"
              onclick="getLocation()"
            >
              📍 Add Location
            </button>
          </div>

          <!-- LOCATION -->
          <div class="mb-3">
            <label class="form-label">Pickup Location</label>
            <input
              type="text"
              class="form-control"
              name="location"
              id="id_location"
              readonly
            />
          </div>

          <!-- ================= PHOTO UPLOAD (NEW) ================= -->
          <div class="mb-3">
            <label class="form-label">Upload Item Photo</label>

            <!-- Desktop -->
            <div
              id="drop-area"
              class="border border-2 rounded p-3 text-center"
              style="border-style: dashed; display: none;"
            >
              <p class="mb-1">📂 Drag & drop image here</p>
              <p class="text-muted">or</p>
              <label class="btn btn-outline-primary btn-sm">
                Choose Image
                <input
                  type="file"
                  name="photo"
                  id="photoInput"
                  accept="image/*"
                  hidden
                />
              </label>
            </div>

            <!-- Mobile -->
            <div id="mobile-upload" style="display: none;">
              <input
                type="file"
                class="form-control"
                name="photo"
                id="photoInputMobile"
                accept="image/*"
                capture="environment"
              />
              <small class="text-muted">
                Take photo or choose from gallery
              </small>
            </div>

            <img
              id="preview"
              class="img-fluid mt-3 rounded"
              style="max-height: 220px; display: none;"
            />
          </div>

          <!-- PICKUP DATE -->
          <div class="mb-3">
            <label class="form-label">Pickup Date</label>
            <input
              type="date"
              class="form-control"
              name="pickup_date"
              required
            />
          </div>

          <button type="submit" class="btn btn-success w-100">
            Submit Donation
          </button>
        </form>
      </div>
    </div>

    <!-- ================= SCRIPTS ================= -->
    <script>
      function getCategory() {
        const description = document.getElementById("id_description").value;
        fetch("{% url 'ai_category' %}?description=" + encodeURIComponent(description))
          .then((res) => res.json())
          .then((data) => {
            document.getElementById("id_category").value = data.category;
          });
      }

      function getLocation() {
        navigator.geolocation.getCurrentPosition((pos) => {
          document.getElementById("id_location").value =
            "Lat: " + pos.coords.latitude + ", Lng: " + pos.coords.longitude;
        });
      }

      /* PHOTO UPLOAD LOGIC */
      const isMobile = /Android|iPhone|iPad/i.test(navigator.userAgent);
      const dropArea = document.getElementById("drop-area");
      const mobileUpload = document.getElementById("mobile-upload");
      const preview = document.getElementById("preview");

      let input;

      if (isMobile) {
        mobileUpload.style.display = "block";
        input = document.getElementById("photoInputMobile");
      } else {
        dropArea.style.display = "block";
        input = document.getElementById("photoInput");
      }

      input.addEventListener("change", () => {
        const file = input.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          preview.src = reader.result;
          preview.style.display = "block";
        };
        reader.readAsDataURL(file);
      });

      if (!isMobile) {
        dropArea.addEventListener("dragover", (e) => e.preventDefault());
        dropArea.addEventListener("drop", (e) => {
          e.preventDefault();
          input.files = e.dataTransfer.files;
          input.dispatchEvent(new Event("change"));
        });
      }
    </script>
  </body>
</html>
