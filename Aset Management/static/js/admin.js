document.addEventListener("DOMContentLoaded", function() {
    function toggleFields() {
        var kategori = document.querySelector("#id_kategori").value;
        
        var routerFields = ["id_jumlah_port_wan", "id_jumlah_port_lan", "id_kecepatan_wireless", "id_protocol_supported"];
        var switchFields = ["id_jumlah_port_switch", "id_managed", "id_poe_support"];

        routerFields.forEach(function(field) {
            document.getElementById(field).closest('.form-row').style.display = (kategori === "Router") ? "" : "none";
        });

        switchFields.forEach(function(field) {
            document.getElementById(field).closest('.form-row').style.display = (kategori === "Switch") ? "" : "none";
        });
    }

    document.querySelector("#id_kategori").addEventListener("change", toggleFields);
    toggleFields();
});
