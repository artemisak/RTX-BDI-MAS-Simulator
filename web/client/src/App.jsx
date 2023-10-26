import { createContext } from "react";
import PatientsTable from "./components/PatientsTable";
import { Box } from "@chakra-ui/react";
import InternsTable from "./components/InternsTable";
import PhysiciansTable from "./components/PhysiciansTable";
import { useConnection } from "./hooks/useConnection";

export const PatientsDataContext = createContext();
export const InternsDataContext = createContext();
export const PhysiciansDataContext = createContext();

function App() {
  const { patientsData, physiciansData, internsData } = useConnection(
    "http://localhost:5000"
  );

  return (
    <Box m={20}>
      <PatientsDataContext.Provider value={patientsData}>
        <PatientsTable />
      </PatientsDataContext.Provider>

      <InternsDataContext.Provider value={internsData}>
        <InternsTable />
      </InternsDataContext.Provider>

      <PhysiciansDataContext.Provider value={physiciansData}>
        <PhysiciansTable />
      </PhysiciansDataContext.Provider>
    </Box>
  );
}

export default App;
