import { Theme } from '@mui/material'
import makeStyles from '@mui/styles/makeStyles'
import React from 'react'
import { Project } from '../../types'
import CustomHubSelection from '../project/CustomHubSelection'
import ProjectDateSection from './ProjectDateSection'
import ProjectLocationSearchBar from './ProjectLocationSearchBar'

const useStyles = makeStyles<Theme>((theme) => {
  return {
    root: {
      [theme.breakpoints.up('md')]: {
        display: 'flex',
        justifyContent: 'space-between',
      },
    },
    verticalFlex: {
      flexGrow: 1,
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'left',
    },
  }
})

type Args = {
  projectData: Project
  handleSetProjectData: Function
  locationInputRef: any
  locationOptionsOpen: boolean
  setLocationOptionsOpen: Function
  errors: any
}

export default function ProjectTimeAndPlaceSectionAndCustomHub({
  projectData,
  handleSetProjectData,
  locationInputRef,
  locationOptionsOpen,
  setLocationOptionsOpen,
  errors,
}: Args) {
  const classes = useStyles()

  function handleUpdateSelectedHub(hubName: string) {
    handleSetProjectData({ hubName: hubName })
  }

  return (
    <div className={classes.root}>
      <ProjectDateSection
        projectData={projectData}
        handleSetProjectData={handleSetProjectData}
        errors={errors}
      />
      <div className={classes.verticalFlex}>
        <ProjectLocationSearchBar
          projectData={projectData}
          handleSetProjectData={handleSetProjectData}
          locationInputRef={locationInputRef}
          locationOptionsOpen={locationOptionsOpen}
          handleSetLocationOptionsOpen={setLocationOptionsOpen}
        />
        <CustomHubSelection
          currentHubName={projectData.hubName ?? ''}
          handleUpdateSelectedHub={handleUpdateSelectedHub}
        />
      </div>
    </div>
  )
}
