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
import { InternsDataContext } from "../App";

export default function InternsTable() {
  const data = useContext(InternsDataContext);
  return (
    <TableContainer mb={20}>
      <Text>Interns</Text>
      <Table variant="striped">
        <Thead>
          <Tr>
            <Th sx={{ textAlign: "left !important" }} isNumeric>
              Id
            </Th>
            <Th sx={{ textAlign: "left !important" }}>Name</Th>
            <Th sx={{ textAlign: "left !important" }} isNumeric>
              Efficiency
            </Th>
          </Tr>
        </Thead>
        <Tbody>
          {data?.map((el, i) => (
            <Tr key={el.id + i}>
              <Td>{el.id}</Td>
              <Td>{el.name}</Td>
              <Td>{el.efficiency}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </TableContainer>
  );
}
