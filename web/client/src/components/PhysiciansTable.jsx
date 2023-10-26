import {
  ListItem,
  OrderedList,
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
            <Th sx={{ textAlign: "left !important" }} isNumeric>
              Id
            </Th>
            <Th sx={{ textAlign: "left !important" }}>Name</Th>
            <Th sx={{ textAlign: "left !important" }}>Qualification</Th>
            <Th sx={{ textAlign: "left !important" }}>Workload</Th>
            <Th sx={{ textAlign: "left !important" }}>Live queue</Th>
            <Th sx={{ textAlign: "left !important" }}>History</Th>
          </Tr>
        </Thead>
        <Tbody>
          {data?.map((el, i) => {
            return (
              <Tr key={el.id + i}>
                <Td>{el.id}</Td>
                <Td>{el.name}</Td>
                <Td>{el.qualification}</Td>
                <Td>{el.workload}</Td>
                <Td>
                  <OrderedList>
                    {el._pipeline.map((lineEl) => {
                      for (let key in lineEl) {
                        return (
                          <ListItem key={key}>
                            Id: {key}, Name: {lineEl[key]}
                          </ListItem>
                        );
                      }
                    })}
                  </OrderedList>
                </Td>
                <Td>
                  <OrderedList>
                    {el.completed.map((completedEl) => {
                      for (let key in completedEl) {
                        return (
                          <ListItem key={key}>
                            Id: {key}, Name: {completedEl[key]}
                          </ListItem>
                        );
                      }
                    })}
                  </OrderedList>
                </Td>
              </Tr>
            );
          })}
        </Tbody>
      </Table>
    </TableContainer>
  );
}
