async function openModal(resourceId) {
  const modal = document.getElementById('resourceModal');
  const modalBody = document.getElementById('modal-body');
  const fullViewBtn = document.getElementById("fullViewBtn");
  
  // Show modal immediately
  modal.style.display = 'block';
  modalBody.innerHTML = '<p>Loading resource...</p>';

  try {
    const response = await fetch(`/dashboard/${resourceId}/preview`);
    if (!response.ok) throw new Error('Failed to load resource');

    const html = await response.text();
    modalBody.innerHTML = html;
    fullViewBtn.href = `/dashboard/${resourceId}/view`;
  } catch (error) {
    modalBody.innerHTML = `<p style="color:red;">Error: ${error.message}</p>`;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById('resourceModal');
  const closeBtn = document.getElementById('closeModal');


  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  });
});