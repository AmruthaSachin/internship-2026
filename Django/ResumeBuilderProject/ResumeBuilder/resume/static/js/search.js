async function searchEmployee() {

    const searchText = document.getElementById("searchBox").value.trim();

    const results = document.getElementById("results");

    results.innerHTML = "";

    if (searchText === "") {

        alert("Please enter Employee ID or Name");

        return;
    }

    try {

        const response = await fetch(`/api/employees/?search=${searchText}`);

        const employees = await response.json();

        if (employees.length === 0) {

            results.innerHTML = "<h3>No Employee Found</h3>";

            return;
        }

        employees.forEach(employee => {

            results.innerHTML += `

            <div class="employee-card">

                <div class="employee-info">

                    <h3>${employee.first_name} ${employee.last_name}</h3>

                    <p><strong>Employee ID:</strong> ${employee.employee_id}</p>

                    <p><strong>Designation:</strong> ${employee.designation}</p>

                </div>

                <div>

                    <a
                        href="/api/resume/${employee.employee_id}/download/"
                        class="download-btn"
                    >
                        Download Resume
                    </a>

                </div>

            </div>

            `;

        });

    }

    catch(error){

        console.log(error);

        alert("Something went wrong.");

    }

}