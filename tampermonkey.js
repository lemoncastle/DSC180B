// ==UserScript==
// @name         IFCB auto-download (HDR, features, class scores)
// @namespace    https://ifcb.caloos.org/
// @version      1.0
// @description  Download IFCB files once links are populated
// @match        https://ifcb.caloos.org/bin*
// @grant        GM_download
// @connect      ifcb.caloos.org
// @run-at       document-idle
// ==/UserScript==

(function () {
    'use strict';

    const IDS = [
        "download-hdr",
        "download-features",
        "download-class-scores"
    ];

    function tryDownload() {
        let found = 0;

        IDS.forEach(id => {
            const a = document.getElementById(id);
            if (a && a.href && !a.href.endsWith("#")) {
                console.log("Downloading:", a.href);
                const link = document.createElement("a");
                link.href = a.href;
                link.download = "";
                document.body.appendChild(link);
                link.click();
                link.remove();
                found++;
            }
        });

        if (found === 0) {
            console.log("Waiting for IFCB links...");
            setTimeout(tryDownload, 1000);
        }
    }

    function goToNextBin() {
        const next = document.getElementById("next-bin");
        if (!next) {
            console.log("something broke");
            return;
        }
        console.log("next bin");
        next.click();
    }

    setTimeout(tryDownload, 5000);
    setTimeout(goToNextBin, 10000);

})();

// first bin is https://ifcb.caloos.org/timeline?dataset=scripps-pier-ifcb-183&bin=D20250101T185049_IFCB183
// last bin is https://ifcb.caloos.org/timeline?dataset=scripps-pier-ifcb-183&bin=D20251231T235627_IFCB183