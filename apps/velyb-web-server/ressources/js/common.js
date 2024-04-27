// Notification should disappear after 3 seconds
const notificationElement = document.getElementById('notification');

if (notificationElement) {
    setTimeout(() => {
        notificationElement.classList.add('hide');
        notificationElement.remove()
    }, 3000);
}

/**
 * 
 * @param {string} message le message d'erreur
 * @param {string} type error | success
 */
export const createNotification = (message, type) => {
    const main = document.getElementsByTagName('main')[0];
    const element = document.createElement('p');
    element.id = 'notification';
    element.innerText = message;
    element.classList.add(type);
    main.appendChild(element);

    setTimeout(() => {
        element.classList.add('hide');
        element.remove()
    }, 3000);

}