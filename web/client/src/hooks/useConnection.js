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
        const parsedData = JSON.parse(event.data);
        let entity = parsedData;

        if (typeof parsedData === "string") {
          entity = JSON.parse(parsedData);
        }

        console.log(entity);

        switch (entity.role) {
          case "Patient":
            setPatientsData((prev) => {
              if (prev.some((el) => el.id === entity.id)) {
                return prev;
              }
              return [...prev, entity];
            });
            break;
          case "Physician":
            setPhysiciansData((prev) => {
              if (prev.some((el) => el.id === entity.id)) {
                return prev;
              }
              return [...prev, entity];
            });
            break;
          case "Intern":
            setInternsData((prev) => {
              if (prev.some((el) => el.id === entity.id)) {
                return prev;
              }
              return [...prev, entity];
            });
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
