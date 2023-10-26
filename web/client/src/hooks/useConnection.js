import { useEffect, useMemo, useState } from "react";

export function useConnection(url) {
  const [listening, setListening] = useState(false);
  const [patientsData, setPatientsData] = useState([]);
  const [physiciansData, setPhysiciansData] = useState([]);
  const [internsData, setInternsData] = useState([]);

  useEffect(() => {
    if (!listening) {
      const events = new EventSource(`${url}/events`);

      events.onmessage = (event) => {
        const allData = JSON.parse(event.data);
        const group = allData.group;
        const entities = JSON.parse(allData?.data);

        switch (group) {
          case "Patient":
            setPatientsData(entities);
            break;
          case "Physician":
            setPhysiciansData(entities);
            break;
          case "Intern":
            setInternsData(entities);
            break;
          default:
            return;
        }
      };
      setListening(true);
    }
  }, [listening, url]);

  useEffect(() => {
    if (listening) {
      fetch(`${url}/all`);
    }
  }, [listening, url]);

  return useMemo(
    () => ({
      patientsData,
      physiciansData,
      internsData,
    }),
    [internsData, patientsData, physiciansData]
  );
}
