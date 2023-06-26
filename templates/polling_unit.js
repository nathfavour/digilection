$(document).ready(function() {
    // Get the LGA dropdown box.
    var lgaDropdown = $('#lga_id');

    // Get the Ward dropdown box.
    var wardDropdown = $('#ward_id');

    // Get the Polling Unit dropdown box.
    var pollingUnitDropdown = $('#polling_unit_id');

    // Get the Announced Pu Results table.
    var announcedPuResultsTable = $('#announced_pu_results');

    // When the LGA dropdown box is changed, update the Ward dropdown box.
    lgaDropdown.on('change', function() {
        var lgaId = $(this).val();

        // Get the wards from the Ward table that belong to the selected LGA.
        var wards = Ward.objects.filter(lga_id=lgaId);

        // Create a new array of options for the Ward dropdown box.
        var wardOptions = [];

        // Loop through the wards and create a new option for the Ward dropdown box.
        wards.forEach(function(ward) {
            wardOptions.push(
                new Option(ward.name, ward.id)
            );
        });

        // Set the new array of options for the Ward dropdown box.
        wardDropdown.html(wardOptions);
    });

    // When the Ward dropdown box is changed, update the Polling Unit dropdown box.
    wardDropdown.on('change', function() {
        var wardId = $(this).val();

        // Get the polling units from the PollingUnit table that belong to the selected Ward.
        var pollingUnits = PollingUnit.objects.filter(ward_id=wardId);

        // Create a new array of options for the Polling Unit dropdown box.
        var pollingUnitOptions = [];

        // Loop through the polling units and create a new option for the Polling Unit dropdown box.
        pollingUnits.forEach(function(pollingUnit) {
            pollingUnitOptions.push(
                new Option(pollingUnit.name, pollingUnit.id)
            );
        });

        // Set the new array of options for the Polling Unit dropdown box.
        pollingUnitDropdown.html(pollingUnitOptions);
    });

    // When the Polling Unit dropdown box is changed, fetch the Announced Pu Results for the selected Polling Unit.
    pollingUnitDropdown.on('change', function() {
        var pollingUnitId = $(this).val();

        // Fetch the Announced Pu Results for the selected Polling Unit.
        $.ajax({
            url: '/announced_pu_results/' + pollingUnitId,
            success: function(data) {
                // Update the Announced Pu Results table with the data from the Ajax request.
                announcedPuResultsTable.html(data);
            }
        });
    });
});
