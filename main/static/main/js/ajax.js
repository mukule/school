<script>
// Assuming you have a select element for the class and stream fields with the IDs 'id_class_admitted' and 'id_stream' respectively

// Function to fetch filtered streams based on the selected class
function getFilteredStreams(classId) {
  $.ajax({
    url: '/get_filtered_streams/',  // Replace with the appropriate URL
    type: 'GET',
    data: {
      class_id: classId
    },
    success: function (response) {
      var streams = response.streams;
      var streamSelect = $('#id_stream');

      // Clear previous options
      streamSelect.empty();

      // Add new options for filtered streams
      for (var i = 0; i < streams.length; i++) {
        var stream = streams[i];
        streamSelect.append($('<option></option>').attr('value', stream.id).text(stream.name));
      }
    },
    error: function (error) {
      console.log(error);
    }
  });
}

// Event listener for the class field change
$('#id_class_admitted').on('change', function () {
  var classId = $(this).val();
  if (classId) {
    getFilteredStreams(classId);
  } else {
    // Clear the streams field if no class is selected
    $('#id_stream').empty();
  }
});

</script>