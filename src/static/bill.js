const form = document.getElementById("bill-form");
const submitButton = form.querySelector('input[type="submit"]');
const status = document.getElementById("form-status");
const idleLabel = submitButton.value;

function setBusy(busy) {
  submitButton.disabled = busy;
  submitButton.value = busy ? "Calculating..." : idleLabel;
  status.hidden = !busy;
  form.setAttribute("aria-busy", String(busy));
}

// Listen for "submit" (not "click") so the browser's own validation runs first
// and the button is only locked once the form is really being sent.
form.addEventListener("submit", (event) => {
  if (submitButton.disabled) {
    event.preventDefault();
    return;
  }
  setBusy(true);
});

// Coming back with the browser's Back button can restore the page from cache
// with the button still locked, so reset it.
window.addEventListener("pageshow", (event) => {
  if (event.persisted) {
    setBusy(false);
  }
});
