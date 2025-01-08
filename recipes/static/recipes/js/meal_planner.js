document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Handle add meal button clicks
    document.querySelectorAll('.add-meal-btn').forEach(button => {
        button.addEventListener('click', function() {
            const date = this.dataset.date;
            document.querySelector('#addMealModal input[name="date"]').value = date;
        });
    });

    // Handle previous/next month navigation
    document.querySelector('.prev-month').addEventListener('click', function() {
        // TODO: Implement month navigation
    });

    document.querySelector('.next-month').addEventListener('click', function() {
        // TODO: Implement month navigation
    });

    // Initialize meal tags as tooltips
    document.querySelectorAll('.meal-tag').forEach(tag => {
        new bootstrap.Tooltip(tag);
    });
});