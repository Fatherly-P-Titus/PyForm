// Initialize Materialize components
document.addEventListener('DOMContentLoaded', function() {
    // Initialize sidenav
    var sidenavElems = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenavElems);
    
    // Initialize materialboxed for images
    var materialboxElems = document.querySelectorAll('.materialboxed');
    M.Materialbox.init(materialboxElems);
    
    // Initialize scrollspy for navigation
    var scrollspyElems = document.querySelectorAll('.scrollspy');
    M.ScrollSpy.init(scrollspyElems, {
        throttle: 100,
        scrollOffset: 100
    });
    
    // Initialize date picker
    var dateElems = document.querySelectorAll('.datepicker');
    M.Datepicker.init(dateElems, {
        format: 'yyyy-mm-dd',
        yearRange: [1900, new Date().getFullYear()],
        autoClose: true
    });
    
    // Form reset handler
    document.querySelector('button[type="reset"]').addEventListener('click', function() {
        document.getElementById('imagePreview').style.display = 'none';
    });
});

// Image preview functionality
document.getElementById('image').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const preview = document.getElementById('imagePreview');
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        
        reader.readAsDataURL(file);
    } else {
        preview.style.display = 'none';
    }
});

// Form submission handler
document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="material-icons left">hourglass_empty</i> Processing...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/submit', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            M.toast({
                html: `<i class="material-icons left">check_circle</i> ${data.message}`,
                classes: 'green',
                displayLength: 4000
            });
            
            // Reset form
            form.reset();
            document.getElementById('imagePreview').style.display = 'none';
            
            // Show success message with user details
            setTimeout(() => {
                M.toast({
                    html: `
                        <div style="text-align: left;">
                            <h6>Registration Details:</h6>
                            <p><strong>Name:</strong> ${data.user.first_name} ${data.user.surname}</p>
                            <p><strong>Email:</strong> ${data.user.email}</p>
                            <p><strong>Phone:</strong> ${data.user.phone_number}</p>
                        </div>
                    `,
                    classes: 'blue lighten-1',
                    displayLength: 6000
                });
            }, 1000);
            
        } else {
            throw new Error(data.error || 'Submission failed');
        }
        
    } catch (error) {
        M.toast({
            html: `<i class="material-icons left">error</i> ${error.message}`,
            classes: 'red',
            displayLength: 4000
        });
        console.error('Error:', error);
    } finally {
        // Reset button state
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
});

// Phone number formatting
document.getElementById('phone_number').addEventListener('blur', function(e) {
    let phone = e.target.value.trim();
    
    // If starts with 0, convert to +234
    if (phone.startsWith('0')) {
        phone = '+234' + phone.substring(1);
        e.target.value = phone;
    }
    // If starts with 234, add +
    else if (phone.startsWith('234') && !phone.startsWith('+234')) {
        phone = '+' + phone;
        e.target.value = phone;
    }
});

// Real-time validation
document.querySelectorAll('input, textarea').forEach(input => {
    input.addEventListener('blur', function() {
        if (this.hasAttribute('required') && !this.value.trim()) {
            this.classList.add('invalid');
        } else {
            this.classList.remove('invalid');
            this.classList.add('valid');
        }
    });
});

// Change featured image periodically
const images = [
    'https://images.unsplash.com/photo-1518837695005-2083093ee35b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1559028012-481c04fa702d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1511632765486-a01980e01a18?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80'
];

let currentImageIndex = 0;
setInterval(() => {
    currentImageIndex = (currentImageIndex + 1) % images.length;
    document.getElementById('featuredImage').src = images[currentImageIndex];
}, 10000); // Change every 10 seconds



