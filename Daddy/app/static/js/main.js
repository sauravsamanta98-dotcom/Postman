// Daddy - JavaScript utilities

$(document).ready(function() {
    // Add animation on page load
    console.log('Daddy Expense Tracker loaded');
    
    // Date picker default value
    var today = new Date().toISOString().split('T')[0];
    $('input[type="date"]').val(today);
});

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Confirm delete action
function confirmDelete() {
    return confirm('Are you sure you want to delete this item?');
}
