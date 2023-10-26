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
import { PhysiciansDataContext } from "../App";

export default function PhysiciansTable() {
  const data = useContext(PhysiciansDataContext);
  return (
    <TableContainer>
      <Text>Physicians</Text>
      <Table variant="striped">
        <Thead>
          <Tr>
            <Th isNumeric>Id</Th>
            <Th>Name</Th>
            <Th>Qualification</Th>
            <Th>Workload</Th>
            <Th>Live queue</Th>
            <Th>History</Th>
          </Tr>
        </Thead>
        <Tbody>
          {data?.map((el, i) => {
            console.log(el);
            // const liveQueue = JSON.parse(el.liveQueue);
            // const history = JSON.parse(el.history);
            return (
              <Tr key={el.id + i}>
                <Td>{el.id}</Td>
                <Td>{el.name}</Td>
                <Td>{el.qualification}</Td>
                <Td>{el.workload}</Td>
                <Td>{el.liveQueue.length ? el.liveQueue : "-"}</Td>
                <Td>{el.history.length ? el.history : "-"}</Td>
              </Tr>
            );
          })}
        </Tbody>
      </Table>
    </TableContainer>
  );
}
