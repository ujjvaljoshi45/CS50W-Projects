document.addEventListener('DOMContentLoaded', function() {

    const submit = document.querySelector('#submit');
    const newTask = document.querySelector('#task');

    submit.disable = true;

    newTask.onkeyup = () => {
        if (newTask.value.length > 0) {
            submit.disable = false;
        }
        else {
            submit.disable = true;
        }
    }

    document.querySelector('form').onsubmit = () => {
        const task = newTask.value;

        const li = document.createElement('li');
        li.innerHTML = task;
        document.querySelector('#tasks').append(li);

        newTask.value = '';
        submit.disable = true;
        return false;
    }
});