import { gql } from '@apollo/client';

export const ADD_TRAIL_JUNCTION = gql`
  mutation AddTrailJunction($name: String!) {
    createTrailJunction(name: $name) {
      trailJunction {
        id
        name
      }
    }
  }
`;