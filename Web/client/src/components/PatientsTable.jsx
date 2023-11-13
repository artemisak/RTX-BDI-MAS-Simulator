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
            <Th sx={{ textAlign: "left !important" }} isNumeric>
              Id
            </Th>
            <Th
              sx={{
                textAlign: "left !important",
              }}
            >
              Name
            </Th>
            <Th
              sx={{
                textAlign: "left !important",
              }}
              isNumeric
            >
              Physician id
            </Th>
            <Th
              sx={{
                textAlign: "left !important",
              }}
              isNumeric
            >
              Task urgency
            </Th>
            <Th
              sx={{
                textAlign: "left !important",
              }}
              isNumeric
            >
              Task intricate
            </Th>
            <Th
              sx={{
                textAlign: "left !important",
              }}
              isNumeric
            >
              Income time
            </Th>
            <Th
              sx={{
                textAlign: "left !important",
              }}
              isNumeric
            >
              resume time
            </Th>
          </Tr>
        </Thead>
        <Tbody>
          {data?.map((el, i) => (
            <Tr key={el.id + i}>
              <Td>{el.id}</Td>
              <Td>{el.name}</Td>
              <Td>{el.physician_id}</Td>
              <Td>{el.urgency}</Td>
              <Td>{el.intricate}</Td>
              <Td>{el.income_time.split(".")[0]}</Td>
              <Td>{el.resume_time.split(".")[0]}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </TableContainer>
  );
}
