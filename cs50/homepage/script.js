// this functions mimics the htop interface

function updateHtop() {
    // Generate random values (for demonstration)
    let cpuPercentage = Math.floor(Math.random() * 100);
    let memPercentage = Math.floor(Math.random() * 100);
    let tasksCount = Math.floor(Math.random() * 100);
    let uptime = `${Math.floor(Math.random() * 24)}h ${Math.floor(Math.random() * 60)}m`;

    // Update the content
    document.getElementById('htop-content').innerHTML = `
        <pre>
            CPU%   MEM%   TASKS   UPTIME
            ----   ----   -----   ------
            ${cpuPercentage}%     ${memPercentage}%     ${tasksCount}     ${uptime}
        </pre>
    `;
}

// htop-like visualization every 5 s (5000 milliseconds)
setInterval(updateHtop, 5000);

function showHtop() {
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('guide-content').style.display = 'none';
    document.getElementById('htop-content').style.display = 'block';
    updateHtop(); // Initial update on button click
}

function showGuide() {
    document.getElementById('main-content').style.display = 'none';
    document.getElementById('htop-content').style.display = 'none';
    document.getElementById('guide-content').style.display = 'block';
}
