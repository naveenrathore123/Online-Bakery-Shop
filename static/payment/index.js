var stripe = Stripe('pk_test_51KQCMkSAiE1KaIdDMomK17sAuTBr66Q5KVz0wWN5yCFqMkZvqwc5Ob4XyXvReD3fcbo3BDhFRBCpI1zvoVnhDuba00rRNZ23NX');
// var stripe = Stripe('sk_test_51KQCMkSAiE1KaIdDw81NZZtit6lxIOKKPBokHzRWoR6jKQNQMwO9sCBWhLKCDbhgpZAme4sLOOyXPNlZa1ShcRS000ECnVQYN2')
var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

var elements = stripe.elements();

var style = {
    base: {
        color:"#000",
        lineHeight: "2.4",
        fontSize: "16px"
    }
};
var card = elements.create("card", {style: style});
card.mount("#card-element");

card.on('change', function(event) {
    var displayError = document.getElementById('card-errors')
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert alert-info');
    } else {
        displayError.textContent = '';
        $('#card-errors').removeClass('alert alert-info');
    }
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev){
    ev.preventDefault();

    var custName = document.getElementById('custName').value;
    var custAdd = document.getElementById('custAdd').value;
    var custAdd2 = document.getElementById('custAdd2').value;
    var postCode = document.getElementById('postCode').value;

    $.ajax({
        type: 'POST',
        URL: 'http://127.0.0.1:8000/orders/add/',
        data: {
            order_key: clientsecret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: 'post',
        },
        success: function(json) {
            console.log(json.success)
            
            stripe.confirmCardPayment(clientsecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        address: {
                            line1:custAdd,
                            line2:custAdd2
                        },
                        name:  custName
                    },
                }
            }).then(function(result){
                if (result.error){
                    console.log('payment error')
                    console.log(result.error.message);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        console.log('payment processed')
                        // there is a risk of the customer the winodw 
                        // berfore callback execution. Set up a webhook or 
                        // plugin to listen for the payment_intent.succeeded event 
                        // that handles any business critical post-payment actions.
                        window.location.replace('http://127.0.0.1:8000/payment/orderplaced/'); 
                    }
                }
            });
        },
        error: function(xhr, errmsg, err) {},
    });
}); 
