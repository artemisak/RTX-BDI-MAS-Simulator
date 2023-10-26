import {
  Table,
  TableContainer,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import { useContext } from "react";
import { PatientsDataContext } from "../App";

export default function PatientsTable() {
  const data = useContext(PatientsDataContext);
  return (
    <TableContainer mb={20}>
      <Text>Patients</Text>
      <Table variant="striped">
        <Thead>
          <Tr>
            <Th isNumeric>Id</Th>
            <Th>Name</Th>
            <Th isNumeric>Physician id</Th>
            <Th isNumeric>Task urgency</Th>
            <Th isNumeric>Task intricate</Th>
            <Th isNumeric>Income time</Th>
            <Th isNumeric>resume time</Th>
          </Tr>
        </Thead>
        <Tbody>
          {data?.map((el, i) => (
            <Tr key={el.id + i}>
              <Td>{el.id}</Td>
              <Td>{el.name}</Td>
              <Td>{el.physicianId}</Td>
              <Td>{el.taskUrgency}</Td>
              <Td>{el.taskIntricate}</Td>
              <Td>{el.incomeTime.split(".")[0]}</Td>
              <Td>{el.resumeTime.split(".")[0]}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </TableContainer>
  );
}
