$(document).ready(function() {


  // Function to load tasks via AJAX
  function loadTasks() {
    $.ajax({
      url: "/get_task_list/",
      type: "GET",
      success: function(response) {
        var tasks = response.tasks;
        createTaskUI(tasks)

        $(".delete-task-btn").on("click", function() {

            // Get the task ID from the data attribute
            var taskId = $(this).data("task-id");
        
            // Update the modal's delete button data attribute with the task ID
            $("#confirmDeleteBtn").data("task-id", taskId);
        
            // Show the modal
            $("#deleteTaskModal").modal("show");
          });
        
          // Event handler for confirm delete button in modal
          $("#confirmDeleteBtn").unbind().on("click", function() {
            $("#status-filter").val('0')
            $("#priority-filter").val('0')
            // Get the task ID from the delete button's data attribute
            var taskId = $(this).data("task-id");
        
            // Call the function to delete the task
            deleteTask(taskId);
            
            // Hide the modal
            $("#deleteTaskModal").modal("hide");
          });
            // Event handler for cancel button in modal
        $(".cancelDeleteBtn").on("click", function() {
                // Hide the modal
                $("#deleteTaskModal").modal("hide");
        });
        function deleteTask(taskId) {
            // Perform AJAX request to delete the task
            $.ajax({
              url: "/delete_task/" + taskId + "/",
              type: "POST",
    
              success: function(response) {
                // Handle success response
                loadTasks();
                // Refresh the task list or perform any other desired action
              },
              error: function(xhr, status, error) {
                // Handle error response
                console.error(xhr.responseText);
                // Display error message or perform any error handling
              }
            });
          }

      },
      error: function(xhr, status, error) {
        console.error(xhr.responseText);
        // Display error message or perform any error handling
      }
    });




  }

  // Call loadTasks initially to load tasks on page load
  loadTasks();




    // Add Task button click event
    $("#addTaskBtn").click(function() {
      // Clear form inputs and error messages
      $("#titleInput").val("");
      $("#descriptionInput").val("");
      $("#prioritySelect").val("");
      $("#statusSelect").val("");
      $(".error").empty();
    });
  
    // Function to validate the form inputs
    function validateForm(editTaskId) {
        
      var isValid = true;
  
      // Clear previous error messages
      $(".error").empty();
  
      // Validate title field
      var title = $("#titleInput").val();
      if (title.trim() === "") {
        $("#titleError").text("Title is required");
        isValid = false;
      }
  
      // Validate description field
      // var description = $("#descriptionInput").val();
      // if (description.trim() === "") {
      //   $("#descriptionError").text("Description is required");
      //   isValid = false;
      // }
  
      // Validate priority field
      var priority = $("#prioritySelect").val();
      if (priority === null || priority === "") {
        $("#priorityError").text("Priority is required");
        isValid = false;
      }
      
      if(editTaskId){
      // Validate status field
      var status = $("#statusSelect").val();
      if (status === null || status === "") {
        $("#statusError").text("Status is required");
        isValid = false;
      }
     }
      return isValid;
    }



    // edit and add task js 
    var editTaskId = null; // Global variable to store the ID of the task being edited

    // Add Task button click event
    $("#addTaskBtn").click(function() {
      openTaskForm(null); // Open the form with null task ID (add new task)
    });
  
    // Edit Task button click event
    $(document).on("click", ".editTaskBtn", function() {
      var taskId = $(this).data("task-id");
      openTaskForm(taskId); // Open the form with the task ID to be edited
    });
  
    // Form submit event
    $("#taskForm").submit(function(event) {
      
      event.preventDefault();
      // Validate form inputs
      if (!validateForm(editTaskId)) {
        return;
      }
  
      // Get form data
      var title = $("#titleInput").val();
      var description = $("#descriptionInput").val();
      var priority = $("#prioritySelect").val();
      var status = $("#statusSelect").val();
  
      // Create task object
      var task = {
        title: title,
        description: description,
        priority: priority,
        status: status
      };
      // Perform AJAX request to add/edit the task
      $("#status-filter").val('0')
      $("#priority-filter").val('0')
      if(editTaskId){
        var url = "/get_or_edit_task/" + editTaskId + "/"
      }
      else{
        $.ajax({
            url: "/add_task/",
            type: "POST",
            data: task,
            success: function(response) {
            // Handle success response
            if(response.error) {
                console.log(response.error)
            }
            else{
                loadTasks();
                $("#taskModal").modal("hide");
            }
            // Display success message or perform any additional actions
            },
            error: function(xhr, status, error) {
            // Handle error response
            console.error(xhr.responseText);
            // Display error message or perform any error handling
            }
        });
        return

      }
    //   var url = editTaskId ? "/get_or_edit_task/" + editTaskId + "/" : "/add_task";
      $.ajax({
        url: url,
        type: "POST",
        data: task,
        success: function(response) {
          // Handle success response
          loadTasks();
          // Display success message or perform any additional actions
          $("#taskModal").modal("hide"); // Close the modal after adding/editing the task
        },
        error: function(xhr, status, error) {
          // Handle error response
          console.error(xhr.responseText);
          // Display error message or perform any error handling
        }
      });
    });
  
    // Function to open the task form
    function openTaskForm(taskId) {
      editTaskId = taskId; // Set the task ID to be edited
  
      // Clear form inputs and error messages
      $("#titleInput").val("");
      $("#descriptionInput").val("");
      $("#prioritySelect").val("");
      $("#statusSelect").val("");
      $(".error").empty();
  
      // Set form title
      var formTitle = taskId ? "Edit Task" : "Add Task";
      $("#taskModalLabel").text(formTitle);

      // Set form button label
      var submitBtnLabel = taskId ? "Save Changes" : "Add Task";
      $(".submitBtn").text(submitBtnLabel);
      $(".statusSelection").css('display', 'block');

      // Pre-fill form inputs if editing a task
      if (taskId) {

        // Perform AJAX request to fetch the task details
        $.ajax({
          url: "/get_or_edit_task/" + taskId,
          type: "GET",
          success: function(response) {
            // Pre-fill form inputs with task details

            $("#titleInput").val(response.title);
            $("#descriptionInput").val(response.description);
            $("#prioritySelect option[value='" + response.priority + "']").prop("selected", true);
            $("#statusSelect option[value='" + response.status +"']").prop('selected', true);

           // $("#prioritySelect").change();

          },
          error: function(xhr, status, error) {
            // Handle error response
            console.error(xhr.responseText);
            // Display error message or perform any error handling
          }
        });
      }
      else{
        $(".statusSelection").css('display', 'none');

      }
  
      // Open the task form modal
      $("#taskModal").modal("show");
    }
  
    // Function to validate the form inputs
    // function validateForm() {
    //   // Form validation logic
    // }

        
  });
  
  function createTaskUI(tasks){
    // Clear existing task list
    $("#task-list").empty();

    if (tasks.length > 0) {
      // Iterate over tasks and append them to the task list
      $.each(tasks, function(index, task) {
        var taskItem = `
          <li id="task-${task.id}" class="list-group-item">
            <div class="row">
              <div class="col-md-6">
                <h4>${task.task_title}</h4>
                <p>${task.task_description}</p>
                <p>Priority: ${task.task_priority}</p>
                <p>Status: ${task.task_status}</p>
              </div>
              <div class="col-md-6 text-right">
                <button type="button" class="btn btn-primary editTaskBtn" data-task-id="${task.id}">
                  Edit Task
                </button>
                <button class="btn btn-danger delete-task-btn" data-task-id="${task.id}">Delete</button>
              </div>
            </div>
          </li>
          <br> 
        `;

        $("#task-list").append(taskItem);
      });
    } else {
      // Display message for no tasks found
      $("#task-list").append("<li class='list-group-item'>No tasks found.</li>");
    }

}
        //Priority filter ajax call
        $('#priority-filter').change(function() {
          $("#status-filter").val('0')

          var priority = $(this).val();
      
          $.ajax({
            url: '/filter_task_priority/',
            method: 'GET',
            data: { priority: priority },
            success: function(response) {
              // Handle the response data here
              var tasks = response.tasks
              createTaskUI(tasks)
              console.log(response);
              // You can update your UI or perform other operations with the received data


              $(".delete-task-btn").unbind().on("click", function() {
                // Get the task ID from the data attribute
                var taskId = $(this).data("task-id");
            
                // Update the modal's delete button data attribute with the task ID
                $("#confirmDeleteBtn").data("task-id", taskId);
            
                // Show the modal
                $("#deleteTaskModal").modal("show");
              });
            

        
            },
            error: function(xhr, errmsg, err) {
              // Handle error case
              console.log(errmsg);
            }
                      
          });

        });
    
        //Status filter ajax call
        $('#status-filter').change(function() {
          $("#priority-filter").val('0')
          var status = $(this).val();
      
          $.ajax({
            url: '/filter_task_status/',
            method: 'GET',
            data: { status: status },
            success: function(response) {
              // Handle the response data here
              var tasks = response.tasks
              createTaskUI(tasks)
              console.log(response);
              // You can update your UI or perform other operations with the received data
              
            $(".delete-task-btn").unbind().on("click", function() {
            
            // Get the task ID from the data attribute
            var taskId = $(this).data("task-id");
        
            // Update the modal's delete button data attribute with the task ID
            $("#confirmDeleteBtn").data("task-id", taskId);
        
            // Show the modal
            $("#deleteTaskModal").modal("show");
          });
        
    
            },
            error: function(xhr, errmsg, err) {
              // Handle error case
              console.log(errmsg);
            }
          });
        });
  